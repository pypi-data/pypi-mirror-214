from __future__ import annotations
import inspect
from pathlib import Path
from django.db import migrations
from ...db import get_sql_file_data


def get_migration_path(stack_index=1):
    migration_file = Path(inspect.stack()[stack_index].filename)
    return migration_file.stem


def get_migration_dir(stack_index=1):
    migration_file = Path(inspect.stack()[stack_index].filename)
    migration_name = migration_file.stem
    return migration_file.parent.joinpath(migration_name)


def get_sql_file_operations(*paths: Path|str, **kwargs) -> list[migrations.RunSQL]:
    if not paths:
        paths = [get_migration_dir(stack_index=2)]
    return [migrations.RunSQL(sql=data.sql, reverse_sql=data.reverse_sql) for data in get_sql_file_data(*paths, **kwargs)]
