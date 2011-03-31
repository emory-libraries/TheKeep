class OldDMRouter(object):
    """Custom database router to ensure that all database operations on models in
    the old_dm application use the old_dm database."""

    db_name = 'old_dm'
    appname = 'old_dm'

    def db_for_read(self, model, **hints):
        "Point all operations on old_dm models to old_dm db"
        if model._meta.app_label == self.appname:
            return self.db_name
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on old_dm models to old_dm db"
        if model._meta.app_label == self.appname:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if both models are in old_dm."
        if obj1._meta.app_label == self.appname and obj2._meta.app_label == self.appname:
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure that only old_dm models are synced to old_dm db"
        if db == self.db_name:
            return model._meta.app_label == self.appname
        elif model._meta.app_label == self.appname:
            return False
        return None

