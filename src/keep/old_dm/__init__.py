from django.conf import settings

from eulcore.django.testsetup import starting_tests, finished_tests

_stored_databases = None
_stored_database_routers = None

# old_dm uses a separate database
# To simplify database setup required for testing,
# removing old_dm databasea and database_router from django settings

def _disable_old_dm_db(sender, **kwargs):
    global _stored_databases
    global _stored_database_routers

    _stored_databases = getattr(settings, "DATABASES", None).copy()
    _stored_database_routers = getattr(settings, "DATABASE_ROUTERS", None)

    del settings.DATABASES['old_dm']
    del settings.DATABASE_ROUTERS


def _restore_old_dm_db(sender, **kwargs):
    global _stored_databases
    global _stored_database_routers

    if _stored_databases is not None:
        settings.DATABASES = _stored_databases

    if _stored_database_routers is not None:
        settings.DATABASE_ROUTERS = _stored_database_routers


starting_tests.connect(_disable_old_dm_db)
finished_tests.connect(_restore_old_dm_db)
