from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from eulexistdb.exceptions import DoesNotExist, ReturnedMultiple
from keep.common.fedora import Repository
from keep.collection.models import CollectionObject, FindingAid
from keep.common.utils import solr_interface
import csv


class Command(BaseCommand):
    '''Create :class:`~keep.collection.models.CollectionObject` objects
    based on corresponding :class:`~keep.collection.models.FindingAid` EAD.

    Takes the PID for the numbering scheme object that the collections should
    belong to (will be used to ensure the correct document is found when searching
    for EAD, and created collections will belong to the specified numbering scheme
    object).  Also takes a list of collection ids; for each id specified, this script
    will look for the corresponding EAD document within the requested numbering
    scheme and generate a new :class:`~keep.collection.models.CollectionObject`.
    '''
    help = '''Extensive report by collection that is outputed into csv file:

'''

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-n',
            dest='dryrun',
            action='store_true',
            help="Report what would be done."),
        )

    def handle(self, **options):
        verbosity = int(options['verbosity'])

        errors = 0

        solr = solr_interface()

        with open('collection_report.csv', 'wb') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['ark_uri', 'object_type','pid','duration','content_model','has_original','title','content_size','researcher_access','label','content_format','state','collection_source_id','type','original_pid','access_copy_mimetype','access_code','collection_id', 'collection_label', 'isMemberOfCollection','rights','created_year','has_access_copy','access_copy_size'])

            solrquery = solr.query().sort_by('-created')
            for doc in solrquery:
                try:
                    ark_uri = doc['ark_uri']
                except:
                    ark_uri = ''
                try:    
                    object_type = doc['object_type']
                except:
                    object_type = ''
                try:
                    pid = doc['pid']
                except:
                    pid = ''
                try:
                    duration = doc['duration']
                except:
                    duration = ''
                try:
                    content_model = doc['content_model']
                except:
                    content_model = ''
                try:
                    has_original = doc['has_original']
                except:
                    has_original = ''
                try:
                    title = doc['title']
                except:
                    title = ''
                try:
                    content_size = doc['content_size']
                except:
                    content_size = ''
                try:    
                    researcher_access = doc['researcher_access']
                except:
                    researcher_access = ''
                try:
                    label = doc['label']
                except:
                    label = ''
                try:
                    content_format = doc['content_format']
                except:
                    content_format = ''
                try:
                    state = doc['state']
                except:
                    state = ''
                try:
                    collection_source_id = doc['collection_source_id']
                except:
                    collection_source_id = ''
                try:
                    my_type = doc['type']
                except:
                    my_type = ''
                try:
                    original_pid = doc['original_pid']
                except:
                    original_pid = ''
                try:
                    access_copy_mimetype = doc['access_copy_mimetype']
                except:
                    access_copy_mimetype = ''
                try:
                    access_code = doc['access_code']
                except:
                    access_code = ''
                try:
                    collection_id = doc['collection_id']
                except:
                    collection_id = ''
                try:
                    collection_label = doc['collection_label']
                except:
                    collection_label = ''
                try:
                    ismemberofcollection = doc['isMemberOfCollection']
                except:
                    ismemberofcollection = ''
                try:
                    rights = doc['rights']
                except:
                    rights = ''
                try:
                    created_year = doc['created_year']
                except:
                    created_year = ''
                try:
                    has_access_copy = doc['has_access_copy']
                except:
                    has_access_copy = ''
                try:
                    access_copy_size = doc['access_copy_size']
                except:
                    access_copy_size = ''

                items = [ark_uri, object_type, pid, duration, content_model, has_original, title, content_size, researcher_access, label, content_format, state, collection_source_id, my_type, original_pid, access_copy_mimetype, access_code, collection_id, collection_label, ismemberofcollection, rights, created_year, has_access_copy, access_copy_size]
                array = []
                for item in items:
                    if isinstance(item, basestring):
                        array.append(item.encode('utf-8'))
                    else:
                        array.append(item)
                writer.writerow(array)


