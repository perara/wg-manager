from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        server.c.shared_key.drop()
    except:
        pass


def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        account = Table('server', meta, autoload=True)
        shared_key = Column('shared_key', Text)
        shared_key.create(account)
    except:
        pass
