import datetime
import logging
from sunburnt import sunburnt

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.utils.feedgenerator import Rss201rev2Feed

from eulfedora.util import RequestFailed

from keep.audio.models import AudioObject
from keep.collection.models import CollectionObject
from keep.common.utils import absolutize_url, PaginatedSolrSearch

logger = logging.getLogger(__name__)

class iTunesPodcastsFeedGenerator(Rss201rev2Feed):
    'Extend RSS Feed generator to add fields specific to iTunes podcast feeds'
    def rss_attributes(self):
        attrs = super(iTunesPodcastsFeedGenerator, self).rss_attributes()
        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        return attrs

    def add_item_elements(self,  handler, item):
        super(iTunesPodcastsFeedGenerator, self).add_item_elements(handler, item)

        # map additional itunes-specific fields

        # subtitle is shown in the description column in itunes - shouldn't be too long
        if item.get('description', ''): # if it's present and isn't None or ''
            handler.addQuickElement(u'itunes:subtitle', item['description'])
        # NOTE: could put more detailed info in the itunes:summary/description (up to 4000 characters)

        # duration is total seconds as integer, which iTunes should be able to handle
        if 'duration' in item and item['duration'] is not None:
            handler.addQuickElement(u'itunes:duration', str(item['duration']))

        # itunes:author will be listed in iTunes artist column
        if 'author_name' in item and item['author_name'] is not None:
            handler.addQuickElement(u'itunes:author', item['author_name'])
        # itunes:keyword is not visible but can be searched
        if 'keywords' in item:
            handler.addQuickElement(u'itunes:keywords', ', '.join(item['keywords']))


def feed_items():
    '''Generate and return a solr query object for all items that
    should be included in the feed.'''
    solr = sunburnt.SolrInterface(settings.SOLR_SERVER_URL)
    search_opts = {
        # restrict to objects in the configured pidspace
        'pid': '%s:*' % settings.FEDORA_PIDSPACE,
        # restrict to audio items by content model
        'content_model': AudioObject.AUDIO_CONTENT_MODEL,
        # restrict to items that are allowed to be accessed
        'researcher_access': True,

        # NB: we'd like to restrict to has_access_copy=True, but for
        # metadata migrations we temporarily want to include some items
        # whose access copies are inferred to exist externally instead of
        # explicitly ingested. as a result, we have to skip this restriction
        # for now, which has the negative side effect of including
        # keep-native (i.e., non-migrated) items whose access copies are not
        # (yet?) available. those items shouldn't be in the feed (since
        # they're not yet properly available) and so we should add this
        # restriction back in as soon as we no longer have inferred external
        # datastreams.
#        'has_access_copy': True,
        }
    
    # sort by date created (newest items at the end of the feed)
    solrquery = solr.query(**search_opts).sort_by('created')
    return solrquery    


class PodcastFeed(Feed):
    '''Podcast Feed for Audio objects with MP3 access copy available.

    Due to limitations in the amount of data iTunes can handle in a single feed,
    this PodcastFeed is designed to paginated content into chunks using the configured
    MAX_ITEMS_PER_PODCAST_FEED setting, and expects to be initialized with a page
    number, e.g.::
    
        url(r'^feeds/(?P<page>[0-9]+)/$', PodcastFeed())
    '''
    
    # set information about this feed
    title = 'The Keep - iTunes Feed'
    description = 'Digitized audio resources from the collections'
    feed_type = iTunesPodcastsFeedGenerator
    # could also set the following feed-level attributes:
    #  owner, itunes subtitle, author, summary; itunes owner, image, category

    def __init__(self, *args, **kwargs):
        self._collection_data = {}
        super(PodcastFeed, self).__init__(*args, **kwargs)

    def get_object(self, request, page):
        # each time someone requests a feed, update the cached collection
        # data. self is persistent across requests here. i'm pretty sure
        # that mod_wsgi/django doesn't share it across threads, but even if
        # it did, it would be ok for threads to stomp on eachother so long
        # as this method caches only global, shared collection data.
        self._collection_data = self._get_collection_data()
        return page

    def _get_collection_data(self):
        solr = sunburnt.SolrInterface(settings.SOLR_SERVER_URL)
        solrquery = solr.query(pid='%s:*' % (settings.FEDORA_PIDSPACE,),
                               content_model=CollectionObject.COLLECTION_CONTENT_MODEL)
        collection_count = solrquery.paginate(rows=0).execute().result.numFound
        collections = solrquery.paginate(rows=collection_count).execute()
        return dict(('info:fedora/' + item['pid'], item) for item in collections)

    def link(self, page):
        return reverse('audio:podcast-feed', args=[page])

    def items(self, page):
        # Find all items that should be included in the feed
        # Until we have a better way to do this, find all Audio objects
        # and then filter out any without compressed audio
        # or with rights that do not allow them to be included

        # NOTE: for simplicity & efficiency (to reduce the number of Fedora API 
        # calls), items are being paginated *before* excluding objects based on
        # rights & compressed audio available - this means that many feeds may have
        # fewer than the configured max items.
        items_per_feed = getattr(settings, 'MAX_ITEMS_PER_PODCAST_FEED', 2000)
        
        solrquery = feed_items()
        # wrap the solr query in a PaginatedSolrSearch object
        # that knows how to translate between django paginator & sunburnt
        pagedsolr = PaginatedSolrSearch(solrquery)

        paginated_objects = Paginator(pagedsolr, per_page=items_per_feed)
        current_chunk = paginated_objects.page(page)
        for obj in current_chunk.object_list:
            logger.debug('items obj %s' % (obj['pid'],))
            yield obj

    def item_title(self, item):
        return item['title']

    def item_description(self, item):
        if 'part' in item:
            return item['part']

    def item_guid(self, item):
        if 'ark_uri' in item:
            return item['ark_uri']
        return item['pid']

        # TODO: should be using item['ark_uri']
        # - won't work reliably until existing objects are updated
        # to store ARK uri in MODS record

    def item_pubdate(self, item):
        # if dateIssued is set, convert to python datetime
        if 'date_issued' in item:
            pub_date = item['date_issued'][0]
            date_parts = [int(p) for p in pub_date.split('-')]
            # if year only, use month 1
            if len(date_parts) < 2:
                date_parts.append(1)
            # if year or year-month only, use day 1
            if len(date_parts) < 3:
                date_parts.append(1)
            return datetime.datetime(*date_parts)

    def item_author_name(self, item):
        # using collection # - collection title
        if 'collection_id' in item:
            collection_id = item['collection_id']
            if collection_id in self._collection_data:
                collection = self._collection_data[collection_id]
                return '%s - %s' %  (collection['source_id'], collection['title'])

    def item_categories(self, item):
        # using top-level numbering scheme (MARBL, University Archives) for category
        categories = []
        if 'collection_id' in item:
            collection_id = item['collection_id']
            if collection_id in self._collection_data:
                collection = self._collection_data[collection_id]
                categories.append(collection['archive_label'])
        return categories

    def item_enclosure_url(self, item):
        # link to audio file - many clients require this to be an absolute url
        if item.get('has_access_copy', False):
            return absolutize_url(reverse('audio:download-compressed-audio', args=[item['pid']]))
        
        # remainder supports old dm file locations (for metadata migrations only)
        collection_pid = item.get('collection_id', '')
        if collection_pid.startswith('info:fedora/'): # it does. strip it.
            collection_pid = collection_pid[len('info:fedora/'):]
        collection = self._collection_data.get(collection_pid, None)
        archive_pid = collection.get('archive_id', '') if collection else ''
        if archive_pid.startswith('info:fedora/'): # it does. strip it.
            archive_pid = archive_pid[len('info:fedora/'):]

        if 'dm1_id' in item and collection_pid and collection and archive_pid:
            marbl_pid = getattr(settings, 'PID_ALIASES', {}).get('marbl', None)
            if archive_pid == marbl_pid:
                if collection['source_id'] == 0:
                     collection_path = 'spec_col/Danowski/'
                else:
                    collection_path = 'spec_col/MSS%d/' % (collection['source_id'],)
            else:
                collection_path = 'univ_arch/SER%d/' % (collection['source_id'],)

            # some items have two dm1_id's: the "old" one and the "new" one.
            # the old ones are always longer than the new ones, and we
            # always want to use them when present, so sort by descending
            # length and use the first (longest=="old")
            ids = sorted(item['dm1_id'], cmp=lambda a,b: cmp(len(b), len(a)))

            old_dm_root = getattr(settings, 'OLD_DM_MEDIA_ROOT', '')
            return '%s%saudio/%s.m4a' % (old_dm_root, collection_path,
                                         ids[0])

    def item_link(self, item):
        return reverse('audio:view', args=[item['pid']])

    def item_enclosure_length(self, item):
        if 'access_copy_size' in item:
            return item['access_copy_size']

    def item_enclosure_mime_type(self, item):
        if 'access_copy_mimetype' in item:
            return item['access_copy_mimetype']

        # metadata migrations:
        if 'dm1_id' in item:
            return 'audio/mp4'

    def item_extra_kwargs(self, item):
        # add any additional data that should be mapped to itunes fields
        pidspace, sep, noid = item['pid'].partition(':')
        ids = [noid]
        if 'dm1_id' in item:
            ids.extend(item['dm1_id'])   # dm1 id or dm1 other id
        info = {
            'keywords': ids
        }
        if 'duration' in item:
            info['duration'] = item['duration']
        return info
