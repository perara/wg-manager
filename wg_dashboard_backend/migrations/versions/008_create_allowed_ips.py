from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        allowed_ips = Column('allowed_ips', Text)
        allowed_ips.create(server)
    except:
        pass


def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        server = Table('server', meta, autoload=True)
        server.c.allowed_ips.drop()
    except:
        pass
