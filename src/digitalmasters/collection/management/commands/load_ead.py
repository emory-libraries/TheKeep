from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from eulcore.existdb.exceptions import DoesNotExist, ReturnedMultiple
from digitalmasters.fedora import Repository
from digitalmasters.collection.models import CollectionObject, FindingAid

class Command(BaseCommand):

    args = 'num-scheme-pid collection-id [...]'

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-n',
            dest='dryrun',
            action='store_true',
            help="Report what would be done, but don't ingest any Fedora objects."),
        )

    def handle(self, numbering_pid, *ids, **options):
        verbosity = int(options['verbosity'])

        repo = Repository()
        numbering = repo.get_object(numbering_pid, type=CollectionObject)
        if not numbering.exists:
            raise CommandError('Numbering scheme %s not found' % (numbering_pid,))
        numbering_title = numbering.mods.content.title

        created = 0
        errors = 0

        for id in ids:
            try:
                fa = FindingAid.find_by_unitid(id, numbering_title)
                coll = fa.generate_collection()
                coll.set_collection(numbering.uri)
                if verbosity:
                    print 'Adding %s for collection %s: %s (from %s)' % (coll.pid, id, coll.mods.content.title, numbering_title)
                if not options['dryrun']:
                    coll.save()
                created += 1
            except DoesNotExist:
                print 'No EAD found for id %s in %s' % (id, numbering_title)
                errors += 1
            except ReturnedMultiple:
                print 'Multiple EADs found for id %s in %s' % (id, numbering_title)
                errors += 1

        if verbosity > 1:
            print '%d records created' % (created,)
            print '%d records failed' % (errors,)
