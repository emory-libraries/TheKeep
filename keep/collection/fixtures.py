from django.conf import settings

from keep.collection.models import CollectionObject
from keep.common.fedora import Repository
from keep import mods

# fixture objects for use with unit tests
# objects are generated each time, so content is reliable
# if a test requires the object be ingested into fedora, the test should ingest and purge

class FedoraFixtures:
    @staticmethod
    def archives(format=None):
        if format == dict:
            return [{'title': nick, 'pid': pid}
                    for nick,pid in settings.PID_ALIASES.iteritems()]
            
        if not hasattr(FedoraFixtures, '_archives'):
            repo = Repository()
            FedoraFixtures._archives = [repo.get_object(pid, type=CollectionObject)
                                        for pid in settings.PID_ALIASES.itervalues()]
        return FedoraFixtures._archives

    @staticmethod
    def rushdie_collection():
        repo = Repository()
        obj = repo.get_object(type=CollectionObject)
        obj.label = 'Salman Rushdie Collection'
        obj.mods.content.title = 'Salman Rushdie Collection'
        obj.mods.content.source_id = '1000'
        obj.set_collection(FedoraFixtures.archives()[1].uri)
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1947, point='start'))
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=2008, point='end'))
        obj.mods.content.create_name()
        obj.mods.content.name.name_parts.append(mods.NamePart(text='Salman Rushdie'))
        return obj

    @staticmethod
    def esterbrook_collection():
        repo = Repository()
        obj = repo.get_object(type=CollectionObject)
        obj.label = 'Thomas Esterbrook letter books'
        obj.mods.content.title = 'Thomas Esterbrook letter books'
        obj.mods.content.source_id = '123'
        obj.set_collection(FedoraFixtures.archives()[2].uri)
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1855, point='start'))
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1861, point='end'))
        obj.mods.content.create_name()
        obj.mods.content.name.name_parts.append(mods.NamePart(text='Thomas Esterbrook'))
        return obj

    @staticmethod
    def englishdocs_collection():
        repo = Repository()
        obj = repo.get_object(type=CollectionObject)
        obj.label = 'English documents collection'
        obj.mods.content.title = 'English documents collection'
        obj.mods.content.source_id = '309'
        obj.set_collection(FedoraFixtures.archives()[1].uri)
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1509, point='start'))
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1805, point='end'))
        return obj

    
