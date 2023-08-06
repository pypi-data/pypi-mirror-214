import logging
from django.contrib.auth import get_user_model
from django.db import migrations
from ...lang import ZUT_ROOT
from ...db import get_sql_file_data
from . import get_migration_dir

logger = logging.getLogger(__name__)
migration_dir = get_migration_dir()


def get_engine(schema_editor):
    if schema_editor.connection.vendor.startswith('postgres'):
        return 'pg'
    else:
        logger.info('skipping zut %s: database vendor: %s', migration_dir.name, schema_editor.connection.vendor)
        return None


def forwards(apps, schema_editor):
    engine = get_engine(schema_editor)
    if not engine:
        return
    
    for data in get_sql_file_data(ZUT_ROOT.joinpath('db', f'sql_{engine}')):
        schema_editor.execute(data.sql)
    
    for data in get_sql_file_data(migration_dir.joinpath(f'sql_{engine}'), user=get_user_model()._meta.db_table):
        schema_editor.execute(data.sql)


def backwards(apps, schema_editor):
    engine = get_engine(schema_editor)
    if not engine:
        return
    
    for data in get_sql_file_data(ZUT_ROOT.joinpath('db', f'sql_{engine}')):
        schema_editor.execute(data.reverse_sql)
    
    for data in get_sql_file_data(migration_dir.joinpath(f'sql_{engine}'), user=get_user_model()._meta.db_table):
        schema_editor.execute(data.reverse_sql)


class Migration(migrations.Migration):
    dependencies = [
        ('zut', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards, atomic=True),
    ]
