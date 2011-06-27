# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from collections import defaultdict
import logging
import re

from django.db import models
from django.contrib.auth. models import User

from keep.audio.models import Rights, AudioObject, SourceTech, CodecCreator, \
     TransferEngineer
from keep.collection.models import CollectionObject
from keep.common.fedora import Repository
from keep import mods

logger = logging.getLogger(__name__)

# referenced collections that are not available in Fedora
MISSING_COLLECTIONS = defaultdict(int)
# items with no collection or series specified
ITEMS_WITHOUT_COLLECTION = set()

class ResourceType(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100, db_column='resource_type')
    class Meta:
        db_table = u'resource_types'
        managed = False

    def __unicode__(self):
        return self.type

class StaffName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    MIGRATED_ID_TYPE = 'dm1'

    class Meta:
        db_table = u'staff_names'
        managed = False

    def __unicode__(self):
        return self.name

    def as_transfer_engineer(self):
        # get values in the form we need them for storing in SourceTech
        # return name, id, id type
        try:
            # do a simple firstname/lastname lookup
            # use the Keep/LDAP account if possible
            first, sep, last = self.name.rpartition(' ')
            # restrict to LDAP via ldap user profile
            user = User.objects.filter(emoryldapuserprofile__isnull=False,
                                       first_name=first, last_name=last).get()
            return (user.get_full_name(), user.username,
                         TransferEngineer.LDAP_ID_TYPE)
        except User.DoesNotExist:
            pass

        # if a corresponding LDAP account was not found, fall back to DM id
        return (self.name, self.id, self.MIGRATED_ID_TYPE)
        
        
        


class Authority(models.Model):
    id = models.IntegerField(primary_key=True)
    authority = models.CharField(max_length=255)
    class Meta:
        db_table = u'authorities'
        managed = False

    def __unicode__(self):
        if self.authority == 'lcsh':
            return 'lcshstring'
        elif self.authority == 'naf':
            return 'nafstring'
        else:
            return self.authority

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=255)
    authority = models.ForeignKey(Authority)
    fieldnames = models.IntegerField()
    class Meta:
        db_table = u'genres'
        managed = False

    def __unicode__(self):
        return '%s [authority = %s, field = %d]' % (self.genre, self.authority.authority, self.fieldnames)

class Name(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    authority = models.ForeignKey(Authority)
    name_type = models.CharField(max_length=50)
    class Meta:
        db_table = u'names'
        managed = False

    def __unicode__(self):
        return '%s [%s, authority=%s]' % (self.name, self.name_type, self.authority.authority)

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    class Meta:
        db_table = u'roles'
        managed = False

    def __unicode__(self):
        return '%s [%s]' % (self.title, self.code)

class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    language = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    class Meta:
        db_table = u'languages'
        managed = False

    def __unicode__(self):
        return '%s [%s]' % (self.language, self.code)

# map old DM locations to Keep top-level collection/owning repository objects
REPOSITORY_LOCATION = {}

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    url = models.URLField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    class Meta:
        db_table = u'locations'
        managed = False

    @property
    def corresponding_repository(self):
        global REPOSITORY_LOCATION
        # if this location has not yet been mapped to a repository object, look it up
        if self.name not in REPOSITORY_LOCATION:
            repos = CollectionObject.top_level()
            for repo in repos:
                # translate DM location labels to Keep repository object labels
                if (self.name == repo.label) or \
                   (self.name.startswith('Emory Archives') and repo.label == 'Emory University Archives') or \
                   (self.name.startswith('MARBL') and repo.label == 'Manuscript, Archives, and Rare Book Library'):
                    REPOSITORY_LOCATION[self.name] = repo.uri
                    break

        if self.name in REPOSITORY_LOCATION:
            return REPOSITORY_LOCATION[self.name]

class Subject(models.Model):
    subject = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)
    authority = models.ForeignKey(Authority)
    fieldnames = models.IntegerField()

    # fieldname codes for type of subject
    geographic = 651
    name_personal = 600
    name_corporate = 610
    name_conference = 611
    topic = 650
    title = 630

    class Meta:
        db_table = u'subjects'
        managed = False

    def __unicode__(self):
        return '%s [authority = %s, field %s]' % (self.subject, self.authority.authority, self.fieldnames)

class AudioContentManager(models.Manager):
    # custom manager to find audio items only, using resource type
    def get_query_set(self):
        # filter on resource type: starting with sound recording, will also match musical & nonmusical variant types
        return super(AudioContentManager, self).get_query_set().filter(resource_type__type__startswith='sound recording')

class Content(models.Model):   # individual item
    'A single Content item; main item-level record, and the basis for migration'
    id = models.IntegerField(primary_key=True)
    record_id_type = models.CharField(max_length=50)
    other_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    collection_number = models.IntegerField()
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    resource_type = models.ForeignKey(ResourceType)
    location = models.ForeignKey(Location)
    abstract = models.TextField()
    toc = models.TextField()
    content_notes = models.TextField()
    completed_by = models.IntegerField()
    completed_date = models.DateTimeField()
    data_entered_by = models.ForeignKey(StaffName, db_column='data_entered_by',
                                        related_name='entered_data', null=True)
    data_entered_date = models.DateTimeField()
    authority_work_by = models.ForeignKey(StaffName, db_column='authority_work_by',
                                          related_name='authority_work', null=True)
    authority_work_date = models.DateTimeField()
    initial_qc_by = models.ForeignKey(StaffName, db_column='initial_qc_by',
                                      related_name='quality_control', null=True)
    initial_qc_date = models.DateTimeField()

    # source_sounds (one to many; most items seem to have 0 or 1)
    genres = models.ManyToManyField(Genre)
    names = models.ManyToManyField(Name, through='NameRole')
    languages = models.ManyToManyField(Language)
    subjects = models.ManyToManyField(Subject)


    # eua_series reverse relation is available, defined on EuarchivesSeries class
    @property
    def series_number(self):
        # there should only ever be one series; not defining as one-to-one because not all contents will have a series
        if self.eua_series.count():
            return self.eua_series.all()[0].series

    @property
    def collection(self):
        'Manuscript or Series number in printable/displayable format, with MARBL/EUA designation'
        if self.collection_number:
            desc = DescriptionData.objects.get(pk=self.collection_number)
            return 'MARBL %d' % desc.mss_number
        elif self.series_number:
            return 'EUA %d' % self.series_number

    @property
    def collection_object(self):
        'Fedora Collection object corresponding to the collection or series number and location for this item'
        num = None
        if self.collection_number:
            desc = DescriptionData.objects.get(pk=self.collection_number)
            num = desc.mss_number
        elif self.series_number:
            num = self.series_number

        if num and self.location:
            #Collection 1002 was the 'catch-all' collection in old DM.
            # Collection 0 should be the catch-all for the new version.
            if self.location.name == 'Emory University Archives' and num == 1002:
                num = 0
            coll = list(CollectionObject.find_by_collection_number(num, self.location.corresponding_repository))
            # if we have one and only one match, we have found the correct object
            if len(coll) == 1:
                return coll[0]

        return None

    # default manager & custom audio-only manager
    objects = models.Manager()
    audio_objects = AudioContentManager()

    class Meta:
        db_table = u'contents'
        managed = False

    def __unicode__(self):
        return '%s' % self.id

    def marked_for_deletion(self):
        return self.title and 'delete' in self.title.lower()

    def as_digital_object_and_fields(self):
        repo = Repository()
        obj = repo.get_object(type=AudioObject)

        row_data = self.descriptive_metadata(obj)
        row_data += self.source_tech_metadata(obj)
        row_data += self.digital_tech_metadata(obj)
        row_data += self.rights_metadata(obj)

        return obj, row_data
        

    # list of fields that will be returned by descriptive_metadata method 
    descriptive_fields = ['Collection', 'ID', 'Other ID', 'Date Created',
                          'Date Issued', 'Title', 'Note', 'Type of Resource',
                          'Record Origin', 'Genre', 'Name', 'Language',
                          'Subjects - Geographic',
                          'Subject - Name (personal)',
                          'Subject - Name (corporate)',
                          'Subject - Name (conference)', 'Subject Topic',
                          'Subject Title', 'Record Changed', 'Record Created']

    def descriptive_metadata(self, obj):
        # print out descriptive fields and return a list of values
        logger.debug('--- Descriptive Metadata ---')
        logger.debug('Collection: %s' % self.collection)

        # we'll be using this a lot below
        modsxml = obj.mods.content

        # warn if no collection number could be found (either EUA or MARBL)
        if self.collection is None:
            ITEMS_WITHOUT_COLLECTION.add(self.id)
            if "DANOWSKI" in obj.label.upper():
                obj.collection_uri = list(CollectionObject.find_by_collection_number(0))[0].uri
            logger.warn('Item %d does not have a collection or series number' % self.id)

        # if there is a collection number, warn if the corresponding collection object could not be found
        elif self.collection_object is None:
            MISSING_COLLECTIONS[self.collection] += 1
            logger.warn('Could not find Collection Object in Fedora for Item %d, collection %s' % (self.id,
                                                                                                   self.collection))

        # otherwise we have a collection
        else:
            obj.collection_uri = self.collection_object.uri

        logger.debug('Identifier: %s' % self.id)
        logger.debug('Other ID: %s' % self.other_id)
        modsxml.dm1_id = self.id
        if self.other_id:
            modsxml.dm1_other_id = self.other_id
        data = [self.collection, self.id, self.other_id]

        # source_sound could be multiple; warn if there is more than one
        for source_sound in self.source_sounds.all():
            logger.debug('Item Date Created: %s' % source_sound.source_date)
            logger.debug('Item Date Issued: %s' % source_sound.publication_date)
            if source_sound.source_date:
                modsxml.create_origin_info()
                modsxml.origin_info.created.append(mods.DateCreated(
                        date=source_sound.source_date,
                        encoding='w3cdtf'))
            if source_sound.publication_date:
                modsxml.create_origin_info()
                modsxml.origin_info.issued.append(mods.DateIssued(
                        date=source_sound.publication_date,
                        encoding='w3cdtf'))
        if self.source_sounds.count() > 1:
            logger.error('Item %d has %d Source Sounds (not repeatable)' % \
                (self.id, self.source_sounds.count()))
        data.extend(['\n'.join(ss.source_date
                               for ss in self.source_sounds.all()
                               if ss.source_date),
                     '\n'.join(ss.publication_date
                               for ss in self.source_sounds.all()
                               if ss.publication_date)])

        logger.debug('Item Title: %s' % unicode(self.title))
        modsxml.title = self.title
        data.append(unicode(self.title))

        all_notes = []
        if self.abstract:
            logger.debug('Item Note: %s [abstract]' % self.abstract)
            modsxml.create_dm1_abstract_note()
            modsxml.dm1_abstract_note.text = unicode(self.abstract)
            all_notes.append('%s [abstract]' % self.abstract)
        if self.content_notes:
            logger.debug('Item Note: %s [content]' % self.content_notes)
            modsxml.create_dm1_content_note()
            modsxml.dm1_content_note.text = self.content_notes
            all_notes.append('%s [content]' % self.content_notes)
        if self.toc:
            logger.debug('Item Note: %s [toc]' % self.toc)
            modsxml.create_dm1_toc_note()
            modsxml.dm1_toc_note.text = self.toc
            all_notes.append('%s [toc]' % self.toc)
        data.append('\n'.join(all_notes))

        logger.debug('Item Type of Resource: %s' % 'sound recording')
        modsxml.resource_type = 'sound recording'
        data.append('sound recording')

        if self.data_entered_by:
            logger.debug('Item recordOrigin: %s' % self.data_entered_by.name)
            modsxml.create_record_info()
            modsxml.record_info.record_origin = 'Originally created in DM1 database'
            data.append(self.data_entered_by.name)
        else:
            data.append(None)

        for genre in self.genres.all():
            logger.debug('Item Genre: %s' % unicode(genre))
            genrexml = mods.Genre(text=genre.genre,
                                  authority=genre.authority)
            modsxml.genres.append(genrexml)
        data.append('\n'.join(unicode(genre) for genre in self.genres.all()))

        for namerole in self.namerole_set.all():
            logger.debug('Item Name (Creator): %s' % unicode(namerole.name))
            logger.debug("Item Name Role: %s" % namerole.role)
            namepartxml = mods.NamePart(text=namerole.name.name)
            rolexml = mods.Role(type='text',
                                authority='marcrelator',
                                text=namerole.role.title)
            namexml = mods.Name(type=namerole.name.name_type,
                                authority=namerole.name.authority)
            namexml.name_parts.append(namepartxml)
            namexml.roles.append(rolexml)
            modsxml.names.append(namexml)
        data.append('\n'.join('%s (%s)' % (unicode(namerole.name), namerole.role)  
                        for namerole in self.namerole_set.all()))

        for lang in self.languages.all():
            logger.debug('Item Language: %s' % unicode(lang))
            langterm = mods.LanguageTerm(type='code',
                                         authority='iso639-2b',
                                         text=lang.code)
            langxml = mods.Language()
            langxml.terms.append(langterm)
            modsxml.languages.append(langxml)
        data.append('\n'.join(unicode(lang) for lang in self.languages.all()))

        # NOTE: documentation has locations:location as db field, which does not exist

        # subjects are filtered into type of subject by field name codes
        geographic_subjects = self.subjects.filter(fieldnames=Subject.geographic)
        for subject in geographic_subjects:
            logger.debug('Item Subject Geographic: %s' % unicode(subject))
            subjectxml = mods.Subject(authority=subject.authority.authority,
                                      geographic=subject.subject)
            modsxml.subjects.append(subjectxml)
        person_name_subjects = self.subjects.filter(fieldnames=Subject.name_personal)
        for subject in person_name_subjects:
            logger.debug('Item Subject Name (personal): %s' % unicode(subject))
            namexml = mods.Name(type='personal')
            namexml.name_parts.append(mods.NamePart(text=subject.subject))
            subjectxml = mods.Subject(authority=subject.authority.authority,
                                      name=namexml)
            modsxml.subjects.append(subjectxml)
        corp_name_subjects = self.subjects.filter(fieldnames=Subject.name_corporate)
        for subject in corp_name_subjects:
            logger.debug('Item Subject Name (corporate): %s' % unicode(subject))
            namexml = mods.Name(type='corporate')
            namexml.name_parts.append(mods.NamePart(text=subject.subject))
            subjectxml = mods.Subject(authority=subject.authority.authority,
                                      name=namexml)
            modsxml.subjects.append(subjectxml)
        conf_name_subjects = self.subjects.filter(fieldnames=Subject.name_conference)
        for subject in conf_name_subjects:
            logger.debug('Item Subject Name (conference): %s' % unicode(subject))
            namexml = mods.Name(type='conference')
            namexml.name_parts.append(mods.NamePart(text=subject.subject))
            subjectxml = mods.Subject(authority=subject.authority.authority,
                                      name=namexml)
            modsxml.subjects.append(subjectxml)
        topic_subjects = self.subjects.filter(fieldnames=Subject.topic)
        for subject in topic_subjects:
            logger.debug('Item Subject Topic: %s' % unicode(subject))
            subjectxml = mods.Subject(authority=subject.authority.authority,
                                      topic=subject.subject)
            modsxml.subjects.append(subjectxml)
        title_subjects = self.subjects.filter(fieldnames=Subject.title)
        for subject in title_subjects:
            logger.debug('Item Subject Title: %s' % unicode(subject))
            subjectxml = mods.Subject(authority=subject.authority.authority,
                                      title=subject.subject)
            modsxml.subjects.append(subjectxml)
        for subject_group in [geographic_subjects, person_name_subjects, corp_name_subjects, conf_name_subjects,
                              topic_subjects, title_subjects]:
            data.append('\n'.join(unicode(subj) for subj in subject_group))

        logger.debug('Item recordChangeDate: %s' % self.modified_at)
        logger.debug('Item recordCreationDate: %s' % self.created_at)
        modsxml.create_record_info()
        if self.modified_at:
            modsxml.record_info.change_date = self.modified_at.isoformat()
        if self.created_at:
            modsxml.record_info.creation_date = self.created_at.isoformat()
        data.extend([self.modified_at, self.created_at])
        
        if not modsxml.is_valid():
            for err in modsxml.validation_errors():
                logger.error('MODS validation error: ' + unicode(err))
        modsxml_s = modsxml.serialize(pretty=True)[:-1] # remove final nl
        logger.debug('MODS:\n' + modsxml_s)
        return data
        
     #Special cases for speed / unit mapping
    def _special_speed_map(self, speed, unit):
        if speed == 'O':
            speed = 'other'
        elif speed =='33':
            speed = '33 1/3'
        elif speed == '7.5' and unit =='ips':
            speed ='7 1/2'
            unit = 'inches/sec'
        return speed, unit

    # fields returned by source_tech_metadata_method
    source_tech_fields = ['Note - General', 'Note - Related Files',
                          'Note - Conservation History', 'Speed',
                          'Item Sub-Location', 'Item Form',
                          'Sound Characteristics', 'Tape - Brand/Stock',
                          'Tape - Housing', 'Tape - Reel Size']

    def source_tech_metadata(self, obj):
        logger.debug('--- Source Technical Metadata ---')
        data = []

        # shortcut reference to source tech xml to be updated below
        st_xml = obj.sourcetech.content

        # Save a reference to source sound associated with this item,
        # as it will be used throughout this method
        sounds = list(self.source_sounds.all())

        notes = [ s.source_note for s in sounds
                  if s.source_note ] + \
                [ s.sound_field for s in sounds
                  if s.sound_field ]
        for note in notes:
            logger.debug('Note - General: %s' % note)
            st_xml.note_list.append(unicode(note))
        data.append('\n'.join(notes))

        relfiles = [ s.related_item for s in sounds
                     if s.related_item ]
        for rel in relfiles:
            logger.debug('Note - Related Files: %s' % rel)
            st_xml.related_files_list.append(unicode(rel))
        if len(relfiles) > 1:
            logger.error('Item %d has %d Note - Related Files fields (not repeatable)' % \
                (self.id, len(relfiles)))
        data.append('\n'.join(relfiles))

        cons = [ s.conservation_history for s in sounds
                 if s.conservation_history ]
        for con in cons:
            logger.debug('Note - Conservation History: %s' % con)
            st_xml.conservation_history_list.append(unicode(con))
        data.append('\n'.join(cons))

        speeds = [ s.speed for s in sounds if s.speed ]
        for speed in speeds:
            logger.debug('Speed: %s (unit: %s)' % (speed.speed, speed.unit))
        if len(speeds) > 1:
            logger.error('Item %d has %d Speed fields (not repeatable)' % \
                (self.id, len(speeds)))
        # if there is exactly one speed, set it in the source tech xml
        elif len(speeds) == 1:
            #adjust speed and/or unit values
            speed[0].speed, speed[0].unit = self._special_speed_map(speed[0].speed, speed[0].unit)
            st_xml.create_speed()
            st_xml.speed.value =  speeds[0].speed
            st_xml.speed.unit = speeds[0].unit
            st_xml.speed.aspect = speeds[0].aspect
        data.append('\n'.join('%s %s' % (self._special_speed_map(speed.speed, speed.unit))
                                            for speed in speeds))

        locs = [ s.item_location for s in sounds
                 if s.item_location ]
        for loc in locs:
            logger.debug('Item Sub-Location: %s' % loc)
        if len(locs) > 1:
            logger.error('Item %d has %d Item Sub-Location fields (not repeatable)' % \
                (self.id, len(locs)))
        # if there is exactly one sublocation, set it in the xml
        elif len(locs) == 1:
            st_xml.sublocation = locs[0]
        data.append('\n'.join(locs))
            
        forms = [ s.form for s in sounds
                  if s.form ]
        for form in forms:
            logger.debug('Item Form: %s' % form.short_form)
            st_xml.form_list.append(form.as_sourcetech_form())
        data.append('\n'.join(f.short_form for f in forms))

        chars = [ s.sound_field for s in sounds
                  if s.sound_field ]
        for char in chars:
            logger.debug('Sound Characteristics: %s' % char)
        if len(chars) > 1:
            logger.error('Item %d has %d Sound Characteristics fields (not repeatable)' % \
                (self.id, len(chars)))
        elif len(chars) == 1:
            # sound characteristic is inconsistently capitalized
            # convert to lower case for best match with keep format
            keepchars = chars[0].lower()
            if keepchars != '' and keepchars != 'None':
                if keepchars not in SourceTech.sound_characteristic_options:
                    logger.warning("Sound characteristic '%s' is not in the options list" \
                        % keepchars)
                st_xml.sound_characteristics = keepchars
        data.append('\n'.join(chars))
            
        stocks = [ s.stock for s in sounds
                   if s.stock ]
        for stock in stocks:
            logger.debug('Tape - Brand/Stock: %s' % stock)
            st_xml.stock_list.append(stock)
        data.append('\n'.join(stocks))
        
        housings = [ s.housing for s in sounds
                     if s.housing ]
        for housing in housings:
            logger.debug('Tape - Housing: %s' % housing.description)
        if len(housings) > 1:
            logger.error('Item %d has %d Tape - Housing fields (not repeatable)' % \
                (self.id, len(housings)))
        # if there is exactly one housing, set it in the xml
        elif len(housings) == 1:
            st_xml.housing = housing.as_sourcetech_housing()
        data.append('\n'.join(h.description for h in housings))

        sizes = [ s.numeric_reel_size for s in sounds
                  if s.numeric_reel_size ]
        for size in sizes:
            logger.debug('Tape - Reel Size: %d (unit: inches)' % size)
        if len(sizes) > 1:
            logger.error('Item %d has %d Tape - Reel Size fields (not repeatable)' % \
                (self.id, len(sizes)))
        # if there is one and only one non-zero/blank reel size, add to xml
        if len(sizes) == 1 and sizes[0]:
            st_xml.create_reel_size()
            st_xml.reel_size.value = sizes[0]
            # all values being migrated are in inches
            st_xml.reel_size.unit = 'inches'
        data.append('\n'.join('%d (unit: inches)' % size for size in sizes))
        
        logger.debug('SourceTech XML:\n' + st_xml.serialize(pretty=True))
        return data

    digital_tech_fields = ['Note - Purpose of Digitization', 'Codec creator',
                           'Transfer Engineer']

    def digital_tech_metadata(self, obj):
        logger.debug('--- Digital Technical Metadata ---')
        data = []

        # shortcut reference to digital tech xml to be updated below
        dt_xml = obj.digitaltech.content

        techs = list(self.sound_source_tech.all())

        purposes = [ tech.methodology for tech in techs
                     if tech.methodology ]
        for purp in purposes:
            logger.debug('Note - Purpose of Digitization: %s' % purp)
            dt_xml.digitization_purpose_list.append(purp)
        data.append('\n'.join(purposes))

        # codec creator object for updating XML
        creators = [ tech.codec_creator for tech in techs
                        if tech.codec_creator ]
        # tuple format for display/CSV output
        creator_tuples = [(c.hardware, c.software, c.id) for c in creators]
        for creator in creator_tuples:
            logger.debug('Codec creator: %s/%s (id=%d)' % creator)
        if len(creators) > 1:
            logger.error('Item %d has %d Codec creator fields (not repeatable)' % \
                (self.id, len(creators)))
        if len(creators) == 1:
            # if there is just one code creator, map to xml
            dt_xml.create_codec_creator()
            dt_xml.codec_creator.id = creators[0].id
            # get hardware, software, & version by id match
            hardware, software, version = creators[0].sourcetech_values()
            dt_xml.codec_creator.hardware_list.extend(hardware)
            dt_xml.codec_creator.software = software
            dt_xml.codec_creator.software_version = version
        data.append('\n'.join('%s/%s [%d]' % creator for creator in creator_tuples))

        sounds = list(self.source_sounds.all())
        engineers = [ s.transfer_engineer for s in sounds
                      if s.transfer_engineer ]
        for engineer in engineers:
            logger.debug('Transfer Engineer: %s (id=%d)' % (engineer.name, engineer.id))
        if len(engineers) > 1:
            logger.error('Item %d has %d Transfer Engineer fields (not repeatable)' % \
                (self.id, len(engineers)))
        if len(engineers) == 1:
            dt_xml.create_transfer_engineer()
            # get name, id, and id type for user (handles LDAP look-up for matches)
            name, id, idtype = engineers[0].as_transfer_engineer()
            dt_xml.transfer_engineer.name = name
            dt_xml.transfer_engineer.id = id
            dt_xml.transfer_engineer.id_type = idtype
        data.append('\n'.join('%s [%d]' % (engineer.name, engineer.id) for engineer in engineers))

        logger.debug('DigitalTech XML:\n' + dt_xml.serialize(pretty=True))

        return data

    # list of fields that will be returned by rights_metadata method
    rights_fields = ['Access Status', 'Copyright Holder Name', 'Copyright Date', 'IP Notes']

    def rights_metadata(self, obj):
        # print out rights fields and return a list of values
        logger.debug('--- Rights Metadata ---')
        data = []
        
        # shortcut reference to rights xml to be updated below
        rights_xml = obj.rights.content
        
        # content could have multiple access_rights; warn if any items actually have more than one
        for rights in self.access_rights.all():
            if rights.restriction:
                logger.debug('Access Status and Code: %s - %s' % (rights.restriction.access_code,
                                                           rights.restriction.access_abbreviation))
            logger.debug('Copyright Holder Name: %s' % unicode(rights.name))
            logger.debug('Copyright Date: %s' % rights.copyright_date)
            logger.debug('IP Notes: %s' % rights.restriction_other)

        if self.access_rights.count() > 1:
            logger.error('Item %d has %d Access Rights fields (not repeatable)' % (self.id,
                                                                                   self.access_rights.count()))
        # if there is just one or zero access rights, migrate any values present
        if self.access_rights.count() <=  1:
            #if 0 rights map value 11
            rights = self.access_rights.all()[0] if self.access_rights.count() == 1 else self.access_rights.get(id='11')[0]
            if rights.restriction:
                rights_xml.create_access_status()
                rights_xml.access_status.code = rights.restriction.access_code
                rights_xml.access_status.text = rights.restriction.access_text
            if rights.name:
                # name only, without authority information
                rights_xml.copyright_holder_name = rights.name.name
            if rights.copyright_date:
                rights_xml.copyright_date = rights.w3cdtf_copyright_date()
            if rights.restriction_other:
                rights_xml.ip_note = rights.restriction_other            


        data.append('\n'.join('%s - %s' % (rights.restriction.access_code, rights.restriction.access_abbreviation)
                                        for rights in self.access_rights.all() if rights.restriction))
        data.append('\n'.join(unicode(rights.name) for rights in self.access_rights.all()))
        data.append('\n'.join('%s' % rights.copyright_date for rights in self.access_rights.all()))
        data.append('\n'.join('%s' % rights.restriction_other for rights in self.access_rights.all()))


        logger.debug('Rights XML:\n' + rights_xml.serialize(pretty=True))

        return data

    # all fields stored for a content
    all_fields = descriptive_fields + \
                 source_tech_fields + \
                 digital_tech_fields + \
                 rights_fields


class NameRole(models.Model):
    'A Name associated with a Content item with a specific role'
    content = models.ForeignKey(Content)
    name = models.ForeignKey(Name)
    role = models.ForeignKey(Role)
    class Meta:
        db_table = u'contents_names'
        managed = False

class Restriction(models.Model):
    'Rights restriction - code & description; associated with AccessRights'
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    class Meta:
        db_table = u'restrictions'
        managed = False

    rights_mapping = {
        # old_dm restriction id : keep.audio.models.Rights accessStatus code
        1: 2,
        5: 2,
        2: 3,
        6: 3,
        7: 4,
        3: 8,
        10: 11,
        11: 11,
        2002: 11,
        # no mappings/no records for old DM rights codes:  4, 8, 9, 2003, 2004
    }

    @property
    def access_code(self):
        # return the equivalent keep.audio.models.Rights access status code for the current restriction id
        return self.rights_mapping[self.id]

    @property
    def access_abbreviation(self):
        # return the migrated access abbreviation based on access code
        return Rights.access_terms_dict[str(self.access_code)].abbreviation

    @property
    def access_text(self):
        # return the migrated access text based on access code
        return Rights.access_terms_dict[str(self.access_code)].text
        

class AccessRights(models.Model):
    'Access rights for a single item; joins Restriction, Content, and Name; adds note & copyright date'
    id = models.IntegerField(primary_key=True)
    restriction = models.ForeignKey(Restriction)
    restriction_other = models.CharField(max_length=255)
    content = models.ForeignKey(Content, related_name='access_rights')
    name = models.ForeignKey(Name)
    copyright_date = models.CharField(max_length=50)
    class Meta:
        db_table = u'access_rights'
        managed = False

    def w3cdtf_copyright_date(self):
        if self.copyright_date:
            # old_dm uses 00 for unknown portions of dates, e.g.
            # 1984-00-00, 2001-03-00, or 0000-00-00
            # Remove 00 values to generate a W3C date, or None
            date = re.sub(r'(0000|-00)', '', self.copyright_date)
            if date == '':
                return None
            return date

class CodecCreatorSound(models.Model):
    id = models.IntegerField(primary_key=True)
    hardware = models.CharField(max_length=100)
    software = models.CharField(max_length=100)
    software_version = models.CharField(max_length=100)
    class Meta:
        db_table = u'codec_creator_sounds'
        managed = False

    def __unicode__(self):
        return unicode(self.id)

    codec_creator_mapping = {
        # old_dm codec_creator_sounds id : keep.audio.models.CodecCreator.configuration
        1: '1', # mac g4
        2: '2', # mac g5
        3: '5', # unknown
    }

    def sourcetech_values(self):
        # returns the value portion of keep.audio.models.CodecCreator.configurations
        # which consists of:
        # hardware, software, software version
        return CodecCreator.configurations[self.codec_creator_mapping[self.id]]

    


class ColorSpaces(models.Model):
    id = models.IntegerField(primary_key=True)
    color_space = models.CharField(max_length=50)
    class Meta:
        db_table = u'color_spaces'
        managed = False

class Conditions(models.Model):
    id = models.IntegerField(primary_key=True)
    condition = models.CharField(unique=True, max_length=150)
    class Meta:
        db_table = u'conditions'
        managed = False

class ContentsConditions(models.Model):
    content_id = models.IntegerField()
    condition_id = models.IntegerField()
    class Meta:
        db_table = u'contents_conditions'
        managed = False


class Form(models.Model):
    id = models.IntegerField(primary_key=True)
    form = models.CharField(max_length=150)
    support_material = models.CharField(max_length=50)
    dates = models.CharField(max_length=50)
    identifying_features = models.TextField()
    source = models.CharField(max_length=255)
    class Meta:
        db_table = u'forms'
        managed = False

    def __unicode__(self):
        return '%s' % self.id

    @property
    def short_form(self):
        form = self.form
        if form.startswith('Sound - '):
            form = form[len('Sound - '):]
        return form

    # mappings between old_dm forms and equivalent keep.audio form options
    form_map = {
        'acetate vinyl shellac - 45 rpm': '45 RPM',
        'audiocassette': 'audio cassette',
        'acetate vinyl shellac - 78 rpm': '78',
        'flexidisc': 'flexi disc',
        'cardboard disc': 'cardboard disc',
        'acetate vinyl shellac - 33.3 rpm': 'LP',
        'paper roll': 'other',
        'MP3': 'sound file (MP3)',
        'other disc': 'other',
        'colored plastic disc': 'other',
        'open reel': 'open reel tape',
    }

    def as_sourcetech_form(self):
        '''Convert old_dm Form into an expected value in the
        keep.audio.models.SourceTech.form_options list'''
        form = self.short_form
        # some form options are exactly equivalent; if listed in form_map
        # it needs to be converted
        if form in self.form_map:
            form = self.form_map[form]
        if form not in SourceTech.form_options:
            logger.warn("Source form '%s' is not listed in form options" \
                                % form)
        return form
        

class Speed(models.Model):
    id = models.IntegerField(primary_key=True)
    speed = models.CharField(max_length=255)
    speed_alt = models.CharField(max_length=255)
    format_type = models.CharField(max_length=255)
    class Meta:
        db_table = u'speeds'
        managed = False

    def __unicode__(self):
        return '%s' % self.id

    @property
    def unit(self):
        if self.speed_alt == 'Multiple':
            return 'multiple'
        elif self.speed_alt == 'Other':
            return 'other'
        elif self.speed_alt.endswith('rpm'):
            return 'rpm'
        elif self.speed_alt.endswith('Kilohertz'):
            return 'Kilohertz'
        elif 'ips' in self.speed_alt:
            return 'inches/sec'

    # mappings between old_dm speed to keep.audio speed options
    # format will be speed (in 'value unit' format) : aspect
    # method to generate speed aspects from sourcetech speed_options
    def _generate_speed_aspects():
        aspects = {}
        for st_speed in SourceTech.speed_options:
            # speed options is formulated for django select with grouping
            if isinstance(st_speed[1], tuple):
                # pair will be | delimited value, display form
                for pair in st_speed[1]:
                  aspect, value, unit = pair[0].split('|')
                  if value == unit:   # other
                      lookup_value = value
                  else:
                      lookup_value = '%s %s' % (value, unit)
                  aspects[lookup_value] = aspect
        # skipping Not Applicable (no equivalent in old_dm data for migration)
        return aspects
    # populate speed aspects
    speed_aspects = _generate_speed_aspects()

    @property
    def aspect(self):
        'SourceTech aspect value - calculated from speed & unit'
        if self.unit == 'other':
            lookup_speed = self.unit
        else:
            lookup_speed = '%s %s' % (self.speed, self.unit)
        if lookup_speed in self.speed_aspects:
            return self.speed_aspects[lookup_speed]
        else:
            logger.warn('Could not determine speed aspect for %s' % \
                        lookup_speed)


class SrcMovingImages(models.Model):
    id = models.IntegerField(primary_key=True)
    form_id = models.IntegerField()
    disposition = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    length = models.IntegerField()
    source_note = models.TextField()
    sound_field = models.CharField(max_length=50)
    stock = models.CharField(max_length=255)
    related_item = models.TextField()
    item_location = models.CharField(max_length=255)
    duration = models.DateTimeField()
    content_id = models.IntegerField()
    housing_id = models.IntegerField()
    color = models.CharField(max_length=50)
    polarity = models.CharField(max_length=50)
    base = models.CharField(max_length=50)
    viewable = models.BooleanField()
    dirty = models.BooleanField()
    scratched = models.BooleanField()
    warped = models.BooleanField()
    sticky = models.BooleanField()
    faded = models.BooleanField()
    vinegar_syndrome = models.BooleanField()
    ad_strip = models.CharField(max_length=50)
    ad_strip_date = models.DateTimeField()
    ad_strip_replace_date = models.DateTimeField()
    conservation_history = models.TextField()
    source_date = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=50)
    class Meta:
        db_table = u'src_moving_images'
        managed = False



class DigitalProvenances(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    staff_name_id = models.IntegerField()
    action = models.CharField(max_length=255)
    class Meta:
        db_table = u'digital_provenances'
        managed = False

class EuarchivesSeries(models.Model):
    content = models.ForeignKey(Content, related_name='eua_series', primary_key=True)
    series = models.IntegerField()
    class Meta:
        db_table = u'euarchives_contents_series'
        managed = False

class FeedCollections(models.Model):
    mss_number = models.IntegerField(unique=True)
    class Meta:
        db_table = u'feed_collections'
        managed = False



class Housing(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    class Meta:
        db_table = u'housings'
        managed = False

    def __unicode__(self):
        return '%s' % self.id

    # mappings between old_dm housing options (in lower-case form) to the
    # equivalent keep.audio housing options
    housing_map = {
        'mixed': 'other',
        'extended/amaray case': 'jewel case',
        'slimline case': 'jewel case',
        'archival box': 'cardboard box',
        'non archival box': 'cardboard box',
        'core and archival paper boxes': 'cardboard box',
        'tyvek sleeve': 'paper sleeve',
        'paper jewel case': 'paper sleeve',
    }

    def as_sourcetech_housing(self):
        '''Convert old_dm Housing description into an expected value
        in the keep.audio.models.SourceTech.housing_options list'''

        # housing in old_dm DB looks like:
        #    Moving Image/Sound: Container
        #    Moving Image/Sound/Still Image: None
        # We only care about the second part for this migration
        # TODO: probably requires additional clean-up
        prefix, sep, housing = self.description.partition(': ')
        # keep.audio housing options are all lower case
        housing = housing.lower()
        # if it is listed in our housing map, get the equivalent field
        if housing in self.housing_map:
            housing = self.housing_map[housing]
        # fields should either be in housing_map or match source tech
        # housing fields after conversion to lower-case
        if housing not in SourceTech.housing_options:
            logger.warn("Source housing '%s' is not listed in housing options" \
                                % housing)
        return housing





class ScannerCameras(models.Model):
    id = models.IntegerField(primary_key=True)
    model_name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    software = models.CharField(max_length=100)
    class Meta:
        db_table = u'scanner_cameras'
        managed = False

class SrcStillImages(models.Model):
    id = models.IntegerField(primary_key=True)
    form_id = models.IntegerField()
    dimension_height = models.FloatField()
    dimension_height_unit = models.CharField(max_length=50)
    dimension_width = models.FloatField()
    dimension_width_unit = models.CharField(max_length=50)
    dimension_note = models.CharField(max_length=255)
    disposition = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    source_note = models.TextField()
    related_item = models.TextField()
    item_location = models.CharField(max_length=255)
    content_id = models.IntegerField()
    housing_id = models.IntegerField()
    conservation_history = models.TextField()
    source_date = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=50)
    class Meta:
        db_table = u'src_still_images'
        managed = False

class TargetUrls(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    url = models.CharField(max_length=2000)
    class Meta:
        db_table = u'target_urls'
        managed = False

class Targets(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    pub = models.CharField(max_length=255)
    external_location = models.TextField()
    class Meta:
        db_table = u'targets'
        managed = False

class TechImages(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    format_name_version = models.CharField(max_length=50)
    byte_order = models.CharField(max_length=50)
    compression_scheme = models.CharField(max_length=100)
    color_space_id = models.IntegerField()
    icc_profile = models.CharField(max_length=150)
    y_cb_cr_subsample = models.CharField(max_length=100)
    y_cb_cr_positioning = models.IntegerField()
    y_cb_cr_coefficients = models.CharField(max_length=100)
    ref_bw = models.CharField(max_length=100)
    jpeg2000_profile = models.CharField(max_length=50)
    jpeg2000_class = models.CharField(max_length=50)
    jpeg2000_layers = models.CharField(max_length=50)
    jpeg2000_level = models.CharField(max_length=50)
    mr_sid = models.BooleanField()
    mr_sid_zoom_levels = models.IntegerField()
    file_size = models.IntegerField()
    scanner_camera_id = models.IntegerField()
    methodology = models.CharField(max_length=50)
    image_width = models.FloatField()
    image_length = models.FloatField()
    ppixel_res = models.IntegerField(db_column='pPixel_res') # Field name made lowercase.
    bits_per_sample = models.CharField(max_length=50)
    bits_per_sample_unit = models.CharField(max_length=50)
    samples_per_pixel = models.CharField(max_length=50)
    extra_samples = models.IntegerField()
    target_id = models.IntegerField()
    image_processing = models.CharField(max_length=255)
    gamma = models.CharField(max_length=50)
    scale = models.IntegerField()
    image_note = models.TextField()
    date_captured = models.DateTimeField()
    djvu = models.BooleanField()
    djvu_format = models.CharField(max_length=50)
    deriv_filename = models.CharField(max_length=255)
    file_location = models.CharField(max_length=50)
    digital_provence_id = models.IntegerField()
    url = models.CharField(max_length=1024)
    src_still_image_id = models.IntegerField()
    class Meta:
        db_table = u'tech_images'
        managed = False

class TechMovingImages(models.Model):
    id = models.IntegerField(primary_key=True)
    date_captured = models.DateTimeField()
    format_name = models.CharField(max_length=50)
    resolution = models.IntegerField()
    bits_per_sample = models.IntegerField()
    sampling = models.CharField(max_length=50)
    aspect_ratio = models.IntegerField()
    calibration_ext_int = models.CharField(max_length=50)
    calibrationlocation = models.TextField(db_column='CalibrationLocation') # Field name made lowercase.
    calibration_type = models.CharField(max_length=255)
    data_rate = models.CharField(max_length=50)
    data_rate_mode = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    frame_rate = models.IntegerField()
    note = models.TextField()
    pixels_horizontial = models.IntegerField()
    pixels_vertical = models.IntegerField()
    scan = models.CharField(max_length=50)
    sound = models.BooleanField()
    file_location = models.CharField(max_length=50)
    content_id = models.IntegerField()
    class Meta:
        db_table = u'tech_moving_images'
        managed = False

class TechSound(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.ForeignKey(Content, related_name='sound_source_tech')
    format_name = models.CharField(max_length=50)
    byte_order = models.CharField(max_length=50)
    compression_scheme = models.CharField(max_length=100)
    file_size = models.IntegerField()
    codec_creator_id = models.IntegerField(db_column='codec_creator')
    codec_quality = models.CharField(max_length=50)
    methodology = models.CharField(max_length=50)
    bits_per_sample = models.CharField(max_length=50)
    sampling_frequency = models.CharField(max_length=50)
    sound_note = models.TextField()
    duration = models.CharField(max_length=50)
    date_captured = models.DateTimeField()
    file_location = models.CharField(max_length=50)
    sound_clip = models.TextField()
    digital_provenance_id = models.IntegerField()
    src_sound_id = models.IntegerField()
    class Meta:
        db_table = u'tech_sounds'
        managed = False

    def __unicode__(self):
        return unicode(self.id)

    @property
    def codec_creator(self):
        if self.codec_creator_id:
            return CodecCreatorSound.objects.get(pk=self.codec_creator_id)


class TmpExport(models.Model):
    image = models.IntegerField(db_column='Image') # Field name made lowercase.
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    subject = models.CharField(max_length=255)
    fieldnames = models.IntegerField()
    sa_authority = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    na_authority = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    ga_authority = models.CharField(max_length=255)
    class Meta:
        db_table = u'tmp_export'
        managed = False

class SourceSound(models.Model):
    id = models.IntegerField(primary_key=True)
    reel_size = models.CharField(max_length=50)
    dimension_note = models.CharField(max_length=255)
    disposition = models.CharField(max_length=50)
    gauge = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    length = models.CharField(max_length=50)
    source_note = models.TextField()
    sound_field = models.CharField(max_length=50)
    stock = models.CharField(max_length=255)
    tape_thick = models.CharField(max_length=50)
    track_format = models.CharField(max_length=50)
    related_item = models.TextField()
    item_location = models.CharField(max_length=255)
    content = models.ForeignKey(Content, related_name='source_sounds')
    conservation_history = models.TextField()
    source_date = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=50)
    transfer_engineer = models.ForeignKey(StaffName,
                                          db_column='transfer_engineer_staff_id',
                                          related_name='source_sounds',
                                          null=True)

    # XXX clean up code for these 0-as-null fields:

    # speed_id == 0 means no speed.
    speed_id = models.IntegerField()
    @property
    def speed(self):
        if self.speed_id:
            return Speed.objects.get(pk=self.speed_id)

    # form_id == 0 means no form.
    form_id = models.IntegerField()
    @property
    def form(self):
        if self.form_id:
            return Form.objects.get(pk=self.form_id)

    # housing_id == 0 means no form.
    housing_id = models.IntegerField()
    @property
    def housing(self):
        if self.housing_id:
            return Housing.objects.get(pk=self.housing_id)

    # foreign-key versions of the above fields, for use with querying
    # Content items on related fields.  
    rel_speed = models.ForeignKey(Speed, db_column='speed_id')
    rel_form = models.ForeignKey(Form, db_column='form_id')
    rel_housing = models.ForeignKey(Housing, db_column='housing_id')

    @property
    def numeric_reel_size(self):
        reel_size = self.reel_size
        if reel_size:
            if reel_size.endswith('"'): # all the production items do
                reel_size = reel_size[:-1]
            return int(reel_size)

    class Meta:
        db_table = u'src_sounds'
        managed = False


class DescriptionData(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID')
    main_entry = models.CharField(max_length=150, db_column='Main Entry')
    title_statement = models.CharField(max_length=200, db_column='Title Statement')
    mss_number = models.IntegerField(db_column='MSS Number')
    description_y_n = models.CharField(max_length=5, db_column='Description Y/N')
    record_type = models.CharField(max_length=100, db_column='Type')
    msword_filename = models.CharField(max_length=100, db_column='MSWord File Name')
    rlin_id_number = models.CharField(max_length=50, db_column='RLIN ID Number')
    xml = models.CharField(max_length=50, db_column='XML')
    notes = models.CharField(max_length=100, db_column='Notes')

    class Meta:
        db_table = u'Description Data'
        managed = False

    def __unicode__(self):
        return unicode(self.id)
