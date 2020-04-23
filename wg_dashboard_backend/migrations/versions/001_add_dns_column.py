from sqlalchemy import Table, MetaData, String, Column, Text


def upgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        account = Table('peer', meta, autoload=True)
        dns = Column('dns', Text)
        dns.create(account)
    except:
        pass


def downgrade(migrate_engine):
    try:
        meta = MetaData(bind=migrate_engine)
        dns = Table('peer', meta, autoload=True)
        dns.c.email.drop()
    except:
        pass
