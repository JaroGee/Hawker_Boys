from __future__ import annotations

import logging
from logging.config import fileConfig

from alembic import context

from tms.infra.config import settings
from tms.infra.database import Base, get_engine
import tms.domain.models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")
logger.setLevel(logging.INFO)
config.set_main_option("sqlalchemy.url", str(settings.database_url))
logger.info("Using database URL %s", settings.database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


logger.info("Starting migrations in %s mode", "offline" if context.is_offline_mode() else "online")
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
