import json
import logging
import magic
import os
import shutil
import tempfile
import time
import traceback
import bagit

from django.conf import settings
from django.contrib import messages
from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, Http404, \
    HttpResponseForbidden
from django.shortcuts import render
from django.utils.safestring import mark_safe

from eulcommon.djangoextras.http import HttpResponseUnsupportedMediaType, \
    HttpResponseSeeOtherRedirect
from eulcommon.djangoextras.auth.decorators import permission_required_with_ajax, \
    permission_required_with_403
from eulfedora.models import FileDatastreamObject
from eulfedora.util import RequestFailed, PermissionDenied
from eulfedora.views import raw_datastream, raw_audit_trail


from keep.audio.models import AudioObject
from keep.audio.tasks import queue_access_copy
from keep.collection.models import CollectionObject
from keep.common.fedora import Repository, TypeInferringRepository, history_view, \
    DuplicateContent
from keep.file.forms import UploadForm, DiskImageEditForm, LargeFileIngestForm, \
    SupplementalFileFormSet
from keep.file.models import DiskImage, large_file_uploads
from keep.file.utils import md5sum, dump_post_data


logger = logging.getLogger(__name__)


uploadable_objects = [AudioObject, DiskImage]
# TODO: document requirements for repo objects to be included here
# - list of allowed mimetypes
# - static class method to init from file


# generate list of allowed upload mimetypes based on objects we support
allowed_upload_types = []
for a in uploadable_objects:
    allowed_upload_types.extend(a.allowed_mimetypes)


# TODO: *both* ingest views should check that user has either of these perms:
#@permission_required("file.add_disk_image")
#@permission_required("audio.add_audio")
# and only let them upload the type they have permission to do


@permission_required_with_ajax('common.marbl_allowed')
def upload(request):
    '''Upload file(s) and create new fedora :class:`~keep.audio.models.AudioObject` (s).
    Only accepts audio/x-wav currently.

    There are two distinct ways to upload file. The first case is
    kicked off when "fileManualUpload" exists in the posted form. If
    it does, then this was not a HTML5 browser, and the file upload
    occurs as is usual for a single file upload.

    In the other approach, the file was uploaded via a HTML5 ajax
    upload already. In this case, we are reading in various hidden
    generated form fields that indicate what was uploaded from the
    javascript code.
    '''
    repo = Repository(request=request)

    ctx_dict = {
        # list of allowed file types, in a format suited for passing to javascript
        'js_allowed_types': mark_safe(json.dumps(allowed_upload_types))
    }

    if request.method == 'POST':
        content_type = request.META.get('CONTENT_TYPE', 'application/octet-stream')
        media_type, sep, options = content_type.partition(';')
        # content type is technically case-insensitive; lower-case before comparing
        media_type = media_type.strip().lower()

        # if form has been posted, process & ingest files
        if media_type == 'multipart/form-data':

            # check for a single file upload
            form = UploadForm(request.POST, request.FILES)

            # If form is not valid (i.e., no collection specified, no
            # or mismatched files uploaded), bail out and redisplay
            # form with any error messages.
            if not form.is_valid():
                ctx_dict['form'] = form
                return render(request, 'file/upload.html', ctx_dict)

            # Form is valid. Get collection & check for optional comment
            collection = repo.get_object(pid=form.cleaned_data['collection'],
                                         type=CollectionObject)
            # get user comment if any; default to a generic ingest comment
            comment = form.cleaned_data['comment'] or 'initial repository ingest'
            # get dictionary of file path -> filename, based on form data
            files_to_ingest = form.files_to_ingest()


            # process all files submitted for ingest (single or batch mode)
            if files_to_ingest:
                results = ingest_files(files_to_ingest, collection, comment, request)

                # add per-file ingest result status to template context
                ctx_dict['ingest_results'] = results
                # after processing files, fall through to display upload template

        else:
            # POST but not form data - handle ajax file upload
            return ajax_upload(request)

    # on GET or non-ajax POST, display the upload form
    ctx_dict['form'] = UploadForm()
    # convert list of allowed types for passing to javascript

    return render(request, 'file/upload.html', ctx_dict)
    # NOTE: previously, this view set the response status code to the
    # Fedora error status code if there was one.  Since this view now processes
    # multiple files for ingest, simply returning 200 if processing ends normally.


def ingest_files(files, collection, comment, request):
    '''Ingest a dictionary of files as returned by
    :meth:`keep.files.forms.UploadForm.files_to_ingest`.
    Returns a dictionary reporting per-file ingest success or failure.

    :param files: dictionary of files to be ingested
    :param collection: :class:`~keep.collection.models.CollectionObject` that
        newly ingested objects should be associated with
    :param comment: save message for fedora ingest
    :param request: :class:`~django.http.HttpRequest`, to access Fedora and
        ingest new objects as the logged-in user.
    '''

    # NOTE: using this structure for easy of display in django templates (e.g., regroup)
    results = []

    m = magic.Magic(mime=True)
    for filename, label in files.iteritems():

        file_info = {'label': label}

        # check if file is an allowed type

        # NOTE: for single-file upload, browser-set type is
        # available as UploadedFile.content_type - but since
        # browser mimetypes are unreliable, calculate anyway
        try:
            type = m.from_file(filename)
        except IOError:
            raise Exception('Uploaded file is no longer available for ingest; please try again.')

        type, separator, options = type.partition(';')
        if type not in allowed_upload_types:
            # store error for display on detailed result page
            file_info.update({'success': False,
                              'message': '''File type '%s' is not allowed''' % type})
            # if not an allowed type, no further processing
            results.append(file_info)
            continue

        if collection is None:
            file_info.update({'success': False,
                              'message': '''Collection not selected'''})
            results.append(file_info)
            continue

        # if there is an MD5 file (i.e., file was uploaded via ajax),
        # use the contents of that file as checksum
        if os.path.exists(filename + '.md5'):
            with open(filename + '.md5') as md5file:
                md5 = md5file.read()
        # otherwise, calculate the MD5 (single-file upload)
        else:
            md5 = md5sum(filename)

        # determine what type of object to initialize based on mimetype
        objtype = None
        for t in uploadable_objects:
            if type in t.allowed_mimetypes:
                objtype = t
                break

        # initialize a new object from the file
        obj = objtype.init_from_file(filename, initial_label=label,
                                     request=request, checksum=md5,
                                     mimetype=type)

        # set collection on ingest
        obj.collection = collection

        try:
            # NOTE: by sending a log message, we force Fedora to store an
            # audit trail entry for object creation, which doesn't happen otherwise
            obj.save(comment)
            file_info.update({'success': True, 'pid': obj.pid,
                              'url': obj.get_absolute_url(),
                              'checksum': md5})

            # if audio, needs an additional step:
            if objtype == AudioObject:
                # Start asynchronous task to convert audio for access
                queue_access_copy(obj, use_wav=filename, remove_wav=True)

            # NOTE: could remove MD5 file (if any) here, but MD5 files
            # should be small and will get cleaned up by the cron script

        # special case: detected as duplicate content
        except DuplicateContent as e:
            # mark as failed and generate message with links to records
            links = []
            repo = Repository(request=request)
            for pid in e.pids:
                # use fedora type-inferring logic with list of content models
                # pulled from solr results
                obj = repo.get_object(pid,
                    type=repo.best_subtype_for_object(pid, e.pid_cmodels[pid]))
                # use appropriate object class to get the object url
                links.append('<a href="%s">%s</a>' % (
                    obj.get_absolute_url(), pid)
                )

            msg = mark_safe('%s: %s' % (unicode(e), '; '.join(links)))
            file_info.update({
                'success': False,
                'message': msg
            })

        except Exception as e:
            logger.error('Error ingesting %s: %s' % (filename, e))
            logger.debug("Error details:\n" + traceback.format_exc())
            file_info['success'] = False

            # check for Fedora-specific errors
            if isinstance(e, RequestFailed):
                if 'Checksum Mismatch' in e.detail:
                    file_info['message'] = 'Ingest failed due to a checksum mismatch - ' + \
                        'file may have been corrupted or incompletely uploaded to Fedora'
                else:
                    file_info['message'] = 'Fedora error: ' + unicode(e)

            # non-fedora error
            else:
                file_info['message'] = 'Ingest failed: ' + unicode(e)

        finally:
            # no matter what happened, store results for reporting to user
            results.append(file_info)

    return results



@permission_required_with_ajax('common.marbl_allowed')
def ajax_upload(request):
    """Process a file uploaded via AJAX and store it in a temporary staging
    directory for subsequent ingest into the repository.  The request must
    include the following headers:

         * Content-Disposition, e.g. filename="original_name.wav"
         * Content-MD5: MD5 checksum of the file calculated before upload

    If the file is successfully uploaded and passes checks on file type
    (must be in a configured list of allowed types) and MD5 checksum (the
    checksum calculated for the uploaded file must match the checksum passed in
    the request), then the file will be stored in the ingest staging directory
    and a staging file identifier will be returned in the body of the response.

    To avoid calculating MD5 checksums multiple times, the MD5 for the file
    will also be stored in the ingest staging directory, in a file named the same
    as the staging temporary filename with '.md5' added.

    Note that while the Content-Disposition header is technically intended for use
    in HTTP responses, we're using it here in HTTP requests because it is a
    good fit for our purpose.
    """
    # NOTE: size and type request headers unused?

    # Setup the directory for the file upload.
    staging_dir = settings.INGEST_STAGING_TEMP_DIR
    # FIXME: this should happen only *once* somewhere... where?
    if not os.path.exists(staging_dir):
        os.makedirs(staging_dir)

    try:
        content_disposition = request.META['HTTP_CONTENT_DISPOSITION']
    except KeyError:
        return HttpResponseBadRequest('Content-Disposition header is required',
                                      content_type='text/plain')
    if 'filename=' not in content_disposition:
        return HttpResponseBadRequest('Content-Disposition header must include filename',
                                      content_type='text/plain')
    try:
        client_md5 = request.META['HTTP_CONTENT_MD5']
    except KeyError:
        return HttpResponseBadRequest('Content-MD5 header is required',
                                      content_type='text/plain')

    # content disposition could be something like 'attachment; filename="foo"
    if ';' in content_disposition:
        dispo = content_disposition.split(';')
        for d in dispo:
            if d.strip().startswith('filename='):
                filename = d.strip()[len('filename='):].strip('"')
    else:
        filename = content_disposition[len('filename='):].strip('"')

    file_base, file_extension = os.path.splitext(filename)

    # create a temporary file based on the name of the original file
    with tempfile.NamedTemporaryFile(mode='wb+', suffix=file_extension,
                                     prefix='%s_' % file_base, dir=staging_dir,
                                     delete=False) as upload:
        try:
            content_length = long(request.environ['CONTENT_LENGTH'])
        except:
            content_length = None

        # request.raw_post_data would force us to read the entire file
        # contents into memory before writing it, which could be problematic
        # if the file is large. reading instead straight from wsgi.input
        # allows us to handle it a chunk at a time
        dump_post_data(request.environ['wsgi.input'], upload, content_length)
        upload_file = upload.name

    ingest_file = os.path.basename(upload_file)
    logger.debug('wrote ' + ingest_file)

    try:
        # ignoring request mimetype since it is unreliable
        m = magic.Magic(mime=True)
        mimetype = m.from_file(upload_file)
        logger.debug('mimetype for %s detected as %s' % (ingest_file, mimetype))
        mimetype, separator, options = mimetype.partition(';')
        if mimetype not in allowed_upload_types:
            os.remove(upload_file)
            # send response with status 415 Unsupported Media Type
            return HttpResponseUnsupportedMediaType('File type %s is not allowed' % mimetype,
                                                    content_type='text/plain')
    except Exception as e:
        logger.debug(e)

    # Calculate an MD5 for the uploaded file and compare with the client-calculated
    # MD5 to make sure that the entire file was uploaded correctly
    try:
        start = time.time()
        calculated_md5 = md5sum(upload_file)
        logger.debug('Calculated MD5 checksum for %s: %s (took %f secs)' %
                    (filename, calculated_md5, time.time() - start))
        if calculated_md5 != client_md5:
            logger.debug('calculated md5 %s did not match request MD5 %s' %
                        (calculated_md5, client_md5))
            return HttpResponseBadRequest('Checksum mismatch; uploaded data may be incomplete or corrupted',
                                          content_type='text/plain')

        # if the MD5 check passes, store the MD5 so we don't have to calculate it again
        with open(os.path.join(staging_dir, ingest_file + '.md5'), 'w') as md5file:
            md5file.write(calculated_md5)

    except Exception as e:
        logger.error(e)
        logger.debug("Error details:\n" + traceback.format_exc())

    # success: return the name of the staging file to be used for ingest
    return HttpResponse(ingest_file, content_type='text/plain')


@permission_required_with_403("file.add_disk_image")
def largefile_ingest(request):
    '''Large-file ingest.  On GET, displays a form allowing user to
    select a BagIt that has been uploaded to the configured large-file
    ingest staging area for ingest and association with a collection.
    On POST, generates and ingests a DiskImage object based
    on the contents of the selected BagIt.
    '''
    # ingest content from upload staging area

    context = {}
    template_name = 'file/largefile_ingest.html'
    form = None

    # on POST, process the form and ingest if valid
    if request.method == 'POST':
        form = LargeFileIngestForm(request.POST)

        # if form is not valid, add to context for redisplay with errors
        if not form.is_valid():
            context['form'] = form

        # otherwise, process the form
        else:
            repo = Repository(request=request)

            # Get collection & check for optional comment
            collection = repo.get_object(pid=form.cleaned_data['collection'],
                                         type=CollectionObject)
            # get user comment if any; defauxlt to a generic ingest comment
            comment = form.cleaned_data['comment'] or 'initial repository ingest'
            bag = form.cleaned_data['bag']

            # create dict with file info to add success/failure info
            file_info = {'label': os.path.basename(bag)}

            try:

                # for now, large-file ingest workflow only supports disk images
                obj = DiskImage.init_from_bagit(bag, request)

                # set collection on ingest
                obj.collection = collection

                ## NOTE: Due to a bug in Fedora 3.4 with checksums and
                ## and file uri ingest, the content datastream checksum
                ## must be cleared before ingest; manually check it
                ## after ingest to confirm Fedora calculated what we expect.
                ## This work-around can be removed once we upgrade to Fedora 3.6

                # store datastream checksum that would be sent to fedora
                checksum = obj.content.checksum
                obj._content_checksum = checksum
                # clear it out so Fedora can ingest without erroring
                obj.content.checksum = None

                # file URIs also used for supplemental files; needs
                # to be handled the same way as content datastream
                # - look for any supplementN datastreams, store checksum, and remove
                supplemental_checksums = {}
                for i in range(20):
                    try:
                        dsid = 'supplement%d' % i
                        dsobj = getattr(obj, dsid)
                        supplemental_checksums[dsid] = dsobj.checksum
                        dsobj.checksum = None
                    except AttributeError:
                        # stop iterating - we have found last supplemental file
                        break

                obj.save(comment)

                # remove the ingested bag from large-file staging area
                shutil.rmtree(bag)

                # re-init to allow checking fedora-calculated checksums on
                # supplemental datastreams
                obj = repo.get_object(obj.pid, type=DiskImage)

                # if save succeded (no exceptions), set summary info for diplay
                file_info.update({'success': True,
                                  'pid': obj.pid, 'url': obj.get_absolute_url(),
                                  'checksum': obj.content.checksum})

                # compare checksum generated by Fedora
                # (required because of file uri bug in fedora 3.4;
                #  this can be removed once we upgrade to fedora 3.6+)
                checksum_errors = []

                if obj.content.checksum != checksum:
                    checksum_errors.append('content')

                for dsid, checksum in supplemental_checksums.iteritems():
                    dsobj = obj.getDatastreamObject(dsid)
                    if dsobj.checksum != checksum:
                        checksum_errors.append(dsid)

                if checksum_errors:
                    message = 'Checksum mismatch%s detected on ' + \
                       '%s datastream%s; please contact a repository adminstrator.'''
                    file_info['message'] = message % (
                        'es' if len(checksum_errors) > 1 else '',
                        ', '.join(checksum_errors),
                        's' if len(checksum_errors) > 1 else ''
                    )

            except bagit.BagValidationError as err:
                logger.error(err)
                file_info.update({'success': False, 'message': 'BagIt error: %s' % err})

            # special case: detected as duplicate content
            except DuplicateContent as e:
                # mark as failed and generate message with links to records
                # NOTE: pid url is duplicated logic from web upload view...
                links = []
                for pid in e.pids:
                    # use fedora type-inferring logic with list of content models
                    # pulled from solr results
                    obj = repo.get_object(pid,
                        type=repo.best_subtype_for_object(pid, e.pid_cmodels[pid]))
                    # use appropriate object class to get the object url
                    links.append('<a href="%s">%s</a>' % (
                        obj.get_absolute_url(), pid)
                    )
                msg = mark_safe('%s: %s' % (unicode(e), '; '.join(links)))
                file_info.update({
                    'success': False,
                    'message': msg
                })

            except Exception as err:
                logger.error('Error: %s' % err)
                file_info.update({'success': False, 'message': '%s' % err})

            # report success/failure in the same format as web-upload ingest
            context['ingest_results'] = [file_info]

    # on GET display form to select item(s) for ingest
    # OR on completed valid form post
    files = large_file_uploads()
    if request.method == 'GET' or \
      form is not None and form.is_valid():
        if len(files):
            context['form'] = LargeFileIngestForm()
        else:
            # indicator that no files are available for ingest
            context['no_files'] = True

    return render(request, template_name, context)


@permission_required_with_403("file.view_disk_image")
def view(request, pid):
    '''View a single repository item.

    Not yet implemented; for now, redirects to :meth:`edit` view.
    '''
    # this view isn't implemented yet, but we want to be able to use the
    # uri. so if someone requests the uri, send them straight to the edit
    # page for now.
    return HttpResponseSeeOtherRedirect(reverse('file:edit',
                kwargs={'pid': pid}))


@permission_required_with_403("file.change_disk_image")
def edit(request, pid):
    '''Edit the metadata for a single :class:`~keep.file.models.DiskImage`.'''
    # FIXME: should be generic file (?) or possibly one of several supported files
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=DiskImage)
    try:
        # if this is not actually a disk image, then 404 (object is not available at this url)
        if not obj.has_requisite_content_models:
            raise Http404

        if request.method == 'POST':

            # if data has been submitted, initialize form with request data and object mods
            form = DiskImageEditForm(request.POST, instance=obj)
            if form.is_valid():     # includes schema validation
                # update foxml object with data from the form
                form.update_instance()
                if 'comment' in form.cleaned_data \
                         and form.cleaned_data['comment']:
                     comment = form.cleaned_data['comment']
                else:
                    comment = "update metadata"

                obj.save(comment)
                messages.success(request, 'Successfully updated <a href="%s">%s</a>' % \
                        (reverse('file:edit', args=[pid]), pid))
                # save & continue functionality - same as collection edit
                if '_save_continue' not in request.POST:
                    return HttpResponseSeeOtherRedirect(reverse('site-index'))
                # otherwise - fall through to display edit form again

            # form was posted but not valid
            else:
                # if we attempted to save and failed, add a message since the error
                # may not be obvious or visible in the first screenful of the form
                messages.error(request,
                    '''Your changes were not saved due to a validation error.
                    Please correct any required or invalid fields indicated below and save again.''')

        else:
            # GET - display the form for editing, pre-populated with content from the object
            form = DiskImageEditForm(instance=obj)

        class AdminOpts(object):
            app_label = 'file'
            module_name = 'application'

        # options for generating admin link to edit/add file application db info
        admin_fileapp = AdminOpts()

        return render(request, 'file/edit.html', {'obj': obj, 'form': form,
            'admin_fileapp': admin_fileapp})

    except PermissionDenied:
        # Fedora may return a PermissionDenied error when accessing a datastream
        # where the datastream does not exist, object does not exist, or user
        # does not have permission to access the datastream

        # check that the object exists - if not, 404
        if not obj.exists:
            raise Http404
        # for now, assuming that if object exists and has correct content models,
        # it will have all the datastreams required for this view

        return HttpResponseForbidden('Permission Denied to access %s' % pid,
                                     mimetype='text/plain')

    except RequestFailed as rf:
        # if fedora actually returned a 404, propagate it
        if rf.code == 404:
            raise Http404

        msg = 'There was an error contacting the digital repository. ' + \
              'This prevented us from accessing audio data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, mimetype='text/plain', status=500)


class DatastreamFile(object):
    # object to make a datastream look enough like a file
    # for use with clearable file input as current file contents
    # (used in initial form data for manage_supplements view below)

    def __init__(self, pid, dsid, label):
        self.url = reverse('file:raw-ds', args=(pid, dsid))
        self.label = label

    def __unicode__(self):
        return self.label

    def name(self):
        return self.label


@permission_required_with_403("file.manage_disk_image_supplements")
def manage_supplements(request, pid):
    '''Manage supplemental file datastreams associated with a
    :class:`~keep.file.models.DiskImage`.'''
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=DiskImage)
    if not obj.exists or not obj.has_requisite_content_models:
        raise Http404

    # generate initial data from any existing supplemental datastreams
    initial_data = []
    for s in obj.supplemental_content:
        initial_data.append({'dsid': s.id, 'label': s.label,
            'file': DatastreamFile(obj.pid, s.id, s.label)})

    # on get, just display the form
    if request.method == 'GET':
        formset = SupplementalFileFormSet(initial=initial_data)

    # on post, process the form and any updates/additions
    if request.method == 'POST':
        formset = SupplementalFileFormSet(request.POST, request.FILES,
            initial=initial_data)

        if formset.is_valid():
            m = magic.Magic(mime=True)

            # NOTE: because we currently don't support re-ordering
            # or deletion, simply counting to keep track of datastream ids
            s_id = 0
            modified = 0
            added = 0
            for file_info in formset.cleaned_data:
                # skip empty formset
                if not file_info:
                    continue

                if file_info.get('dsid', None):
                    ds = obj.getDatastreamObject(file_info['dsid'],
                        dsobj_type=FileDatastreamObject)
                    # ds = getattr(obj, file_info['dsid'])
                else:
                    added += 1
                    ds = obj.getDatastreamObject('supplement%d' % s_id,
                        dsobj_type=FileDatastreamObject)

                # only set if changed so datastream isModified is accurate
                if file_info['label'] != ds.label:
                    ds.label = file_info['label']

                # if this is an uploaded file, replace content and calculate mimetype, checksum
                if isinstance(file_info['file'], UploadedFile):

                    filename = file_info['file'].temporary_file_path()
                    mimetype = m.from_file(filename)
                    mimetype, separator, options = mimetype.partition(';')
                    ds.mimetype = mimetype
                    ds.checksum = md5sum(filename)
                    ds.content = file_info['file']

                if ds.exists and ds.isModified():
                    modified += 1

                s_id += 1

            try:
                obj.save('updating supplemental files')

                # summarize number of changes, if any
                if added or modified:
                    msg_add = 'added %d' % added if added else ''
                    msg_update = 'updated %d' % modified if modified else ''
                    msg = 'Successfully %s%s%s supplemental file%s' %  \
                        (msg_add, ' and ' if added and modified else '', msg_update,
                        's' if (added + modified) != 1 else '')
                    messages.success(request, msg)
                else:
                    # possible for the form to be valid but not make any changes
                    messages.info(request, 'No changes made to supplemental content')

                return HttpResponseSeeOtherRedirect(reverse('file:edit', args=[pid]))

            except Exception as e:
                logger.error('Error on supplemental file update: %s' % e)
                logger.debug("Error details:\n" + traceback.format_exc())

                messages.error(request, unicode(e))
                # for now, just redisplay the form with error message

    return render(request, 'file/supplemental_content.html',
        {'obj': obj, 'formset': formset})


### FIXME: these views are currently redundant; consolidate all and make the
# file versions the common ones?

@permission_required_with_403("file.view_disk_image")
def view_datastream(request, pid, dsid):
    'Access raw object datastreams'
    # initialize local repo with logged-in user credentials & call generic view
    # use type-inferring repo to pick up rushdie file or generic arrangement
    response = raw_datastream(request, pid, dsid,
                          repo=TypeInferringRepository(request=request))

    # work-around for email MIME data : display as plain text so it
    # can be viewed in the browser
    if response.get('Content-Type', None) == 'message/rfc822':
        response['Content-Type'] = 'text/plain'
    return response


@permission_required_with_403("file.view_disk_image")
def view_audit_trail(request, pid):
    'Access XML audit trail'
    # initialize local repo with logged-in user credentials & call eulfedora view
    # type shouldn't matter for audit trail
    return raw_audit_trail(request, pid, repo=Repository(request=request))


@permission_required_with_403("file.view_disk_image")
def history(request, pid):
    'Display human-readable audit trail information.'
    return history_view(request, pid, type=DiskImage, template_name='file/history.html')


