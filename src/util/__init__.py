import os
import logging
import logging.config
from environs import Env
from contextlib import contextmanager
import sqlalchemy
from sqlalchemy.orm import sessionmaker


'''
Config and Environment
'''


class Config(object):
    env = Env()
    env.read_env()  # load env variables right away
    _DB_URI = None
    _engine = None
    _SEED_PATH = None

    @property
    def ENVIRONMENT(self):
        return self.env.str("FLASK_ENV", default="production")

    @property
    def DB_URI(self):
        if self._DB_URI is None:
            self._DB_URI = self.env.str("DATABASE_URI")
        return self._DB_URI

    @property
    def SEED_PATH(self):
        if self._SEED_PATH is None:
            self._SEED_PATH = self.env.str("SEED_PATH")
        return self._SEED_PATH

    @property
    def engine(self):
        if self._engine is None:
            url = os.environ.get('DATABASE_URI')
            if not url:
                url = self.DB_URI

            # Queue pool is already there by default, and we can just set the
            # pool parameters without creating or referencing a pool object
            # pool size is how many connections to hand out, 15 is the
            # max, and the pool recycle parameter says that don't keep
            # a connection for more than 900 seconds (15 minutes).
            self._engine = sqlalchemy.create_engine(
                url,
                # json_serializer=custom_dumps,
                # json_deserializer=custom_loads,
                isolation_level='READ_COMMITTED',
                pool_size=5,
                max_overflow=15,
                pool_recycle=900
            )

            # make sure database exists
            # TODO does not work with heroku db
            # if not database_exists(url):
            # create_database(url)

        return self._engine


config = Config()


'''
Logging
'''
logging_config_path = os.path.join(os.path.dirname(__file__), 'logging.ini')
logging.config.fileConfig(logging_config_path)


def loggingFactory(module):
    """
    Factory method that returns a logger generation function with the
    prefix for the modules where it is used.
        _getLogger=loggingFactory('util.alstore')
        logger=_getLogger('method')
        logger.debug('Bla')
    :param module: optional namespace
    :return:
    """

    def getLogger(method=None):
        name = "flashcards." + \
            (module if method is None else module + "." + method)
        return logging.getLogger(name)

    return getLogger


'''
Session Management
'''

Session = None


@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.
    """
    # Init session
    global Session
    if Session is None:
        Session = sessionmaker(bind=config.engine)

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
