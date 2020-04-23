from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        peer = Table('peer', meta, autoload=True)
        shared_key = Column('shared_key', Text)
        shared_key.create(peer)
    except:
        pass


def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        dns = Table('peer', meta, autoload=True)
        dns.c.shared_key.drop()
    except:
        pass
