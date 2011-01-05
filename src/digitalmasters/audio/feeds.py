import datetime

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.core.urlresolvers import reverse

from digitalmasters.audio.models import AudioObject
from digitalmasters.collection.models import get_cached_collection_dict
from digitalmasters.common.utils import absolutize_url
from digitalmasters.fedora import Repository

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
        handler.addQuickElement(u'itunes:subtitle', item['description'])
        # NOTE: could put more detailed info in the itunes:summary/description (up to 4000 characters)

        # duration is total seconds as integer, which iTunes should be able to handle
        if item['duration'] is not None:
            handler.addQuickElement(u'itunes:duration', str(item['duration']))

        # itunes:author will be listed in iTunes artist column
        if item['author_name'] is not None:
            handler.addQuickElement(u'itunes:author', item['author_name'])
        # itunes:keyword is not visible but can be searched
        if 'keywords' in item:
            handler.addQuickElement(u'itunes:keywords', ', '.join(item['keywords']))


class PodcastFeed(Feed):
    '''Podcast Feed for Audio objects with MP3 access copy available. '''
    
    # set information about this feed
    title = 'The Keep - iTunes Feed'
    description = 'Digitized audio resources from the collections'
    feed_type = iTunesPodcastsFeedGenerator
    # could also set the following feed-level attributes:
    #  owner, itunes subtitle, author, summary; itunes owner, image, category

    def link(self):
        return reverse('audio:podcast-feed')

    def items(self):
        # Find all items that should be included in the feed
        # Until we have a better way to do this, find all Audio objects
        # and then filter out any without compressed audio
        # or with rights that do not allow them to be included (rights still TODO)
        search_opts = {
            'type': AudioObject,
            # restrict to objects in configured pidspace
            'pid__contains': '%s*' % settings.FEDORA_PIDSPACE,
            # restrict by cmodel in dc:format
            'format__contains': AudioObject.AUDIO_CONTENT_MODEL,
        }
        repo = Repository()
        # limit to objects with access-copy audio files available
        # TODO: filter on rights
        return (obj for obj in repo.find_objects(**search_opts)
                                if obj.compressed_audio.exists)

    def item_title(self, item):
        return item.mods.content.title

    def item_description(self, item):
        return item.mods.content.part_note

    def item_guid(self, item):
        # globally unique identifier that will never change
        # use full ARK if available
        if item.ark:
            return item.ark_access_uri
        # use item pid only as fallback - should not happen in production
        return item.pid 

    def item_pubdate(self, item):
        # if dateIssued is set, convert to python datetime
        if item.mods.content.origin_info.issued:
            pub_date = item.mods.content.origin_info.issued[0]
            date_parts = [int(p) for p in pub_date.date.split('-')]
            # if year only, use month 1
            if len(date_parts) < 2:
                date_parts.append(1)
            # if year or year-month only, use day 1
            if len(date_parts) < 3:
                date_parts.append(1)
            return datetime.datetime(*date_parts)


    def item_author_name(self, item):
        # using collection # - collection title
        if item.collection_uri:
            collection =  get_cached_collection_dict(str(item.collection_uri))
            return '%s - %s' %  (collection['source_id'], collection['title'])

    def item_categories(self, item):
        # using top-level numbering scheme (MARBL, University Archives) for category
        categories = []
        if item.collection_uri:
            collection =  get_cached_collection_dict(str(item.collection_uri))
            categories.append(collection['collection_label'])
        return categories

    def item_enclosure_url(self, item):
        # link to audio file - MUST be an absolute url
        return absolutize_url(reverse('audio:download-compressed-audio', args=[item.pid]))                    

    def item_enclosure_length(self, item):
        return item.compressed_audio.info.size

    def item_enclosure_mime_type(self, item):
        return item.compressed_audio.mimetype

    def item_extra_kwargs(self, item):
        # add any additional data that should be mapped to itunes fields
        return {
            'duration': item.digitaltech.content.duration,
            'keywords': (item.noid,)    # TODO: add any other ids here after migration
        }
