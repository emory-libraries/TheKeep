from keep.collection.models import CollectionObject
from keep.common.fedora import Repository
from keep import mods

# fixture objects for use with unit tests
# objects are generated each time, so content is reliable
# if a test requires the object be ingested into fedora, the test should ingest and purge

class FedoraFixtures:
    repo = Repository()
    top_level_collections = CollectionObject.top_level()

    @staticmethod
    def rushdie_collection():
        obj = FedoraFixtures.repo.get_object(type=CollectionObject)
        obj.label = 'Salman Rushdie Collection'
        obj.mods.content.title = 'Salman Rushdie Collection'
        obj.mods.content.source_id = '1000'
        obj.set_collection(FedoraFixtures.top_level_collections[1].uri)
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1947, point='start'))
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=2008, point='end'))
        obj.mods.content.create_name()
        obj.mods.content.name.name_parts.append(mods.NamePart(text='Salman Rushdie'))
        return obj

    @staticmethod
    def esterbrook_collection():
        obj = FedoraFixtures.repo.get_object(type=CollectionObject)
        obj.label = 'Thomas Esterbrook letter books'
        obj.mods.content.title = 'Thomas Esterbrook letter books'
        obj.mods.content.source_id = '123'
        obj.set_collection(FedoraFixtures.top_level_collections[2].uri)
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1855, point='start'))
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1861, point='end'))
        obj.mods.content.create_name()
        obj.mods.content.name.name_parts.append(mods.NamePart(text='Thomas Esterbrook'))
        return obj

    @staticmethod
    def englishdocs_collection():
        obj = FedoraFixtures.repo.get_object(type=CollectionObject)
        obj.label = 'English documents collection'
        obj.mods.content.title = 'English documents collection'
        obj.mods.content.source_id = '309'
        obj.set_collection(FedoraFixtures.top_level_collections[1].uri)
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1509, point='start'))
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1805, point='end'))
        return obj

    