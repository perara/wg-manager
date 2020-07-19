from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        v6_address_server = Column('v6_address', VARCHAR, unique=True, nullable=True)
        v6_address_server.create(server)

        meta = MetaData(bind=migrate_engine)
        peer = Table('peer', meta, autoload=True)
        v6_address_peer = Column('v6_address', VARCHAR, nullable=True)
        v6_address_peer.create(peer)
    except:
        pass


def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        server.c.v6_address.drop()

        meta = MetaData(bind=migrate_engine)
        peer = Table('peer', meta, autoload=True)
        peer.c.v6_address.drop()
    except:
        pass


