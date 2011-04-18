from collections import defaultdict

class OldDMRouter(object):
    """Custom database router to ensure that database operations on models
    in the old_dm application use the old_dm database, except for select
    models which need to use the accessions database."""

    appname = 'old_dm'

    db_name_map = defaultdict(lambda: 'old_dm')
    db_name_map['DescriptionData'] = 'accessions'

    def db_for_read(self, model, **hints):
        "Point operations on old_dm models to old_dm or accessions db"
        if model._meta.app_label == self.appname:
            return self.db_name_map[model.__name__]
        return None

    def db_for_write(self, model, **hints):
        "Point operations on old_dm models to old_dm or accessions db"
        if model._meta.app_label == self.appname:
            return self.db_name_map[model.__name__]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if both models are in the old_dm app and the same db."
        if obj1._meta.app_label == self.appname and \
           obj2._meta.app_label == self.appname and \
           self.db_name_map[type(obj1).__name__] == self.db_name_map[type(obj2).__name__]:
            return True
        return None

    def allow_syncdb(self, db, model):
        """Make sure that old_dm models are synced to old_dm or accessions
        db, as appropriate"""
        if db == self.db_name_map[model.__name__]:
            return model._meta.app_label == self.appname
        elif model._meta.app_label == self.appname:
            return False
        return None

