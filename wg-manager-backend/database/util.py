import os

import alembic.command
from alembic.config import Config
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists

import middleware
from database.database import engine, Base, SessionLocal
from database import models
from loguru import logger


def perform_migrations():
    logger.info("Performing migrations...")
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.attributes['configure_logger'] = False

    alembic_cfg.set_main_option('script_location', "migrations")
    alembic_cfg.set_main_option('sqlalchemy.url', str(engine.url))

    alembic.command.upgrade(alembic_cfg, 'head')
    logger.info("Migrations done!")


def setup_initial_database():
    if not database_exists(engine.url):
        logger.info("Database does not exists. Creating initial database...")

        # Create database from metadata
        Base.metadata.create_all(engine)
        logger.info("Database creation done!")

    # Create default user
    _db: Session = SessionLocal()

    # Retrieve user with admin role
    admin_exists = _db.query(models.User.id).filter_by(role="admin").first() is not None

    if not admin_exists:
        logger.info("Admin user does not exists. Creating with env variables ADMIN_USERNAME, ADMIN_PASSWORD")
        env_admin_username = os.getenv("ADMIN_USERNAME")
        env_admin_password = os.getenv("ADMIN_PASSWORD")

        if not env_admin_username:
            raise RuntimeError("Database does not exist and the environment variable ADMIN_USERNAME is set")

        if not env_admin_password:
            raise RuntimeError("Database does not exist and the environment variable ADMIN_PASSWORD is set")

        _db.merge(models.User(
            username=env_admin_username,
            password=middleware.get_password_hash(env_admin_password),
            full_name="Admin",
            role="admin",
            email=""
        ))

    _db.commit()
    _db.close()
