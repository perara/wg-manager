from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        peer = Table('peer', meta, autoload=True)
        keep_alive = Column('keep_alive', Integer)
        keep_alive.create(peer)
    except:
        pass


def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        peer = Table('peer', meta, autoload=True)
        peer.c.keep_alive.drop()
    except:
        pass
