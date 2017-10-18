from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
import os
import sys
sys.path.append(os.getcwd())

from database.models import tables
from database.base import TableBase
target_metadata = TableBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def process_revision_directives(context, revision, directives):
    script = directives[0]

    # erase upgrade operations changing type from TINYINT to BOOLEAN
    remove_upgrade_ops = []
    for table_op in script.upgrade_ops.ops:
        if 'ops' not in table_op.__dict__:
            continue
        remove_ops = []
        for column_op in table_op.ops:
            if not 'existing_type' in column_op.__dict__ or not 'modify_type' in column_op.__dict__:
                continue
            if str(column_op.existing_type) == 'TINYINT(1)' and str(column_op.modify_type) == 'BOOLEAN':
                remove_ops.append(column_op)
                msg = "INFO  [custom process revision directives] Removing misinterpreted type change on"
                msg += " '" + str(column_op.table_name) + "." + str(column_op.column_name) + "'"
                print msg
        temp = [column_op for column_op in table_op.ops if column_op not in remove_ops]
        table_op.ops[:] = temp
        if len(temp) == 0:
            remove_upgrade_ops.append(table_op)
    while len(remove_upgrade_ops) > 0:
        script.upgrade_ops.ops.remove(remove_upgrade_ops[-1])
        remove_upgrade_ops.pop()

    # erase downgrade operations changing type from TINYINT to BOOLEAN
    remove_downgrade_ops = []
    for table_op in script.downgrade_ops.ops:
        if 'ops' not in table_op.__dict__:
            continue
        remove_ops = []
        for column_op in table_op.ops:
            if not 'existing_type' in column_op.__dict__ or not 'modify_type' in column_op.__dict__:
                continue
            if str(column_op.existing_type) == 'BOOLEAN' and str(column_op.modify_type) == 'TINYINT(1)':
                remove_ops.append(column_op)
        temp = [column_op for column_op in table_op.ops if column_op not in remove_ops]
        table_op.ops[:] = temp
        if len(temp) == 0:
            remove_downgrade_ops.append(table_op)
    while len(remove_downgrade_ops) > 0:
        script.downgrade_ops.ops.remove(remove_downgrade_ops[-1])
        remove_downgrade_ops.pop()

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        compare_type=True,
        literal_binds=True,
        sqlalchemy_module_prefix="db.",
        process_revision_directives=process_revision_directives
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            sqlalchemy_module_prefix="db.",
            process_revision_directives=process_revision_directives
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
