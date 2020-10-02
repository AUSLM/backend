from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
import sys

from .models import *
from ..config import cfg


_engine = create_engine(cfg.DB_CONNECTION_STRING)
_Session = sessionmaker(bind=_engine, expire_on_commit=False)


@contextmanager
def get_session():
    session = _Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def check_database():
    try:
        with get_session() as s:
            answer = s.execute("SELECT version();")
            result = [{column: value for column, value in rowproxy.items()} for rowproxy in answer]
            logging.info(f'Successfully connecting to database.\n{str(result[0]["version"])}')
    except Exception as e:
        logging.info(f'Failed to connect to database.\n{str(e)}')
        sys.exit(f'\n----------\nStopped service - try to solve lack of connection to database')


def create_tables(password):
    logging.info('Dropping existing tables')
    try:
        Base.metadata.reflect(_engine)
        Base.metadata.drop_all(_engine)
    except Exception as e:
        logging.info(f'Failed to drop tables.\n{str(e)}')
        sys.exit("Stopped service - try to clean db directly")

    logging.info('Creating tables')
    Base.metadata.create_all(_engine)
    logging.info('Tables was created')
    with get_session() as s:
        root = User(
            email=cfg.SUPER_ADMIN_MAIL,
            password=password,
            name='Super',
            surname='Admin',
            service_status='superadmin',
            confirmation_link='-',
            status='active'
        )
        s.add(root)
    logging.info(f'Root user with mail [{cfg.SUPER_ADMIN_MAIL}] was created')
