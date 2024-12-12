from alembic import command
from alembic.config import Config
from sqlalchemy import Engine

from logger import logger


def migrate(engine: Engine) -> None:
    logger.info("running migrations...")
    _alembic_upgrade_head(engine)
    logger.info("migrations done.")


def _alembic_upgrade_head(engine: Engine) -> None:
    config = Config()
    config.set_main_option("script_location", "alembic")
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")
