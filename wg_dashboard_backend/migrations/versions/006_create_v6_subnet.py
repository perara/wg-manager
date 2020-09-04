from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        peer = Table('server', meta, autoload=True)
        v6_subnet = Column('v6_subnet', INTEGER)
        v6_subnet.create(peer)
    except:
        pass


def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        peer = Table('server', meta, autoload=True)
        peer.c.v6_subnet.drop()
    except:
        pass
