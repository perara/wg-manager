from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        read_only = Column('read_only', INTEGER, default=0)
        read_only.create(server)
    except:
        pass

    try:
        meta = MetaData(bind=migrate_engine)
        peer = Table('peer', meta, autoload=True)
        read_only = Column('read_only', INTEGER, default=0)
        read_only.create(peer)
    except:
        pass

def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        server.c.read_only.drop()
    except:
        pass
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('peer', meta, autoload=True)
        server.c.read_only.drop()
    except:
        pass