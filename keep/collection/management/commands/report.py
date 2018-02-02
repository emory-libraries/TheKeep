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

        collections = open('collections.txt', 'r')
        gb = 1024*1024*1024
        with open('keep_collection_report.csv', 'wb') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['title', 'collection_code', 'library_name','size','object_count','dv_count','mov_count','mpg_count','ad1_count','aff_count','dd_count','e01_count','img_count','iso_count','tar_count','wav_count','status_code_2','status_code_3','status_code_4', 'status_code_5', 'status_code_10','status_code_11','status_code_12','status_code_13'])
            for line in collections:
                print line.strip()
                solrquery = solr.query().filter(title=str(line).strip()).sort_by('-created')
                for doc in solrquery:
                    try:
                        library_name = doc['isMemberOfCollection']
                        library_name = library_name.split('/')[1]
                        library_name = library_name.split("'")[0]
                    except:
                        library_name = ''

                solrquery = solr.query().filter(collection_label=str(line).strip())
                object_count = 0
                size = 0
                dv_count = 0
                mov_count = 0
                mpg_count = 0
                ad1_count = 0
                aff_count = 0
                dd_count = 0
                e01_count = 0
                img_count = 0
                iso_count = 0
                tar_count = 0
                wav_count = 0
                status_code_2 = 0
                status_code_3 = 0
                status_code_4 = 0
                status_code_5 = 0
                status_code_10 = 0
                status_code_11 = 0
                status_code_12 = 0
                status_code_13 = 0
                title = ''
                collection_code = 0
                for doc in solrquery:
                    object_type += 1
                    try:    
                        object_type = doc['object_type']
                    except:
                        object_type = ''

                    if object_type == 'audio':
                        wav_count = wav_count + 1
                        try:
                            size = int(doc['access_copy_size']) + size
                        except:
                            pass

                    
                    elif object_type == 'video':
                        try:
                            size = int(doc['content_size']) + size
                        except:
                            pass

                    elif object_type == 'disk image':
                        try:
                            size = int(doc['content_size']) + size
                        except:
                            pass

                    # collection code
                    try:
                        collection_code = doc['collection_source_id']
                    except:
                        collection_code = ''
                    
                    # access code counting
                    try:
                        access_code = int(doc['access_code'])
                        if access_code == 2:
                            status_code_2 += 1
                        elif access_code == 3:
                            status_code_3 += 1
                        elif access_code == 4:
                            status_code_4 += 1
                        elif access_code == 5:
                            status_code_5 += 1
                        elif access_code == 10:
                            status_code_10 += 1
                        elif access_code == 11:
                            status_code_11 += 1
                        elif access_code == 12:
                            status_code_12 += 1
                        elif access_code == 13:
                            status_code_13 += 1
                    except:
                        pass
                    # content format count       
                    try:
                        content_format = doc['content_format']
                        if content_format == 'AD1':
                            ad1_count += 1
                        elif content_format == 'AFF':
                            aff_count += 1
                        elif content_format == 'DD':
                            dd_count += 1
                        elif content_format == 'E01':
                            e01_count += 1
                        elif content_format == 'IMG':
                            img_count += 1
                        elif content_format == 'ISO':
                            iso_count += 1
                        elif content_format == 'TAR':
                            tar_count += 1
                        elif content_format == 'DV':
                            dv_count += 1
                        elif content_format == 'MOV':
                            mov_count += 1
                        elif content_format == 'MPG':
                            mpg_count += 1
                    except:
                        pass
                                   
                size = float(size) / gb
                writer.writerow([title, collection_code, library_name,size,object_count,dv_count,mov_count,mpg_count,ad1_count,aff_count,dd_count,e01_count,img_count,iso_count,tar_count,wav_count,status_code_2,status_code_3,status_code_4, status_code_5, status_code_10,status_code_11,status_code_12,status_code_13])

                


