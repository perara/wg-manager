from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        keep_alive = Column('keep_alive', Integer)
        keep_alive.create(server)
    except:
        pass


def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        server.c.keep_alive.drop()
    except:
        pass
