from optparse import make_option

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.template.defaultfilters import pluralize

from keep.audio.models import FeedCount
from keep.audio.feeds import feed_items
from keep.common.utils import absolutize_url

class Command(BaseCommand):
    '''Send an email notification if the number of available iTunes
podcast feeds has changed.'''
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-n',
            dest='dry_run',
            action='store_true',
            default=False,
            help='''Report on what would be done, but don't actually ''' + \
            '''send an email or update the stored feed count'''),
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        verbosity = int(options['verbosity'])    # 1 = normal, 0 = minimal, 2 = all
        v_normal = 1

        # use feed search and paginator to determine the number of available feeds
        paginated_feeds = Paginator(feed_items(),
                                settings.MAX_ITEMS_PER_PODCAST_FEED)
        # current total feed count
        feed_count = paginated_feeds.num_pages

        # check the db for last feed count, if any
        try:
            last_count = FeedCount.objects.latest()
        except ObjectDoesNotExist:
            last_count = None

        # special case: if last count is None, store the current value and quit
        if last_count is None:
            print 'No feed count in database; saving current feed count of %d' \
                % feed_count
            if not dry_run:
                FeedCount(count=feed_count).save()
            exit(0)

        # If feed count has not changed, nothing to be done. Quit.
        if feed_count == last_count.count:
            if verbosity >= v_normal:
                print 'No change in the number of available feeds (%d).' \
                    % (feed_count)
                exit(0)

        # if count has changed, send an email and update the database
        if verbosity >= v_normal:
            print 'Last feed count change was %d on %s; current feed count is %d.' \
                % (last_count.count, last_count.date, feed_count)

        message = self.generate_message(last_count, feed_count)
        if verbosity > v_normal:
            print 'Email message content:\n%s' % message
        try:

            if not dry_run:
                send_mail("%s iTunes podcast feed update" % settings.EMAIL_SUBJECT_PREFIX,  # subject
                     message,
                     settings.SERVER_EMAIL,  # from
                     settings.FEED_ADMINS  # recipient list
                     )

                # save the new value if the email was successfully sent
                FeedCount(count=feed_count).save()
                if verbosity >= v_normal:
                    print 'Sent email notice and updated last count to %s.' \
                        % (feed_count)

        except Exception:
            raise CommandError('Failed to send email notification.' +
                '\n-- Please check email server and recipient settings.''')


    def generate_message(self, last_feedcount, current_count):
        '''Generate the text of the email message, with
        details about changes in feeds, including urls to the newly
        available or unavailable feeds.
        '''
        if last_feedcount.count == current_count:
            return None

        message = '\nThe number of available iTunes podcast feeds has changed.\n' \
        + 'There are now %d total iTunes podcast feeds available' % current_count
        # NOTE: for simplicity, not worrying about wording for 1 feed here.

        # number of available feeds has increased
        if current_count > last_feedcount.count:
            diff = current_count - last_feedcount.count
            plural = pluralize(diff)
            message += ' (%d new feed%s).\n' % (diff, plural)
            message += '\nURL%(plural)s for the new feed%(plural)s:\n\n' % \
                {'plural': pluralize(diff)}
            for i in range(last_feedcount.count + 1, current_count + 1):
                message += '  %s\n\n' % absolutize_url(reverse('audio:podcast-feed',
                    args=[i]))

        # number of available feeds has *decreased*
        # (this should be rare, but is possible if content is pulled)
        else:
            diff = (last_feedcount.count - current_count)
            plural = pluralize(diff)
            message += ' (%d fewer feed%s).\n' % (diff, plural)
            message += '\nThe following feed%s (first available %s) are no longer active:\n\n' \
                % (plural, last_feedcount.date)
            for i in range(current_count + 1, last_feedcount.count + 1):
                message += '  %s\n\n' % absolutize_url(reverse('audio:podcast-feed',
                    args=[i]))

        return message


