import sqlalchemy

from sqlalchemy import Integer, Column
from sqlalchemy.orm import relationship, backref
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(sqlalchemy.String, unique=True, index=True)
    password = Column(sqlalchemy.String)
    username = Column(sqlalchemy.String, unique=True)
    full_name = Column(sqlalchemy.String)
    role = Column(sqlalchemy.String)


class WGServer(Base):
    __tablename__ = "server"

    id = Column(Integer, primary_key=True, index=True)
    interface = Column(sqlalchemy.String, unique=True, index=True)
    address = Column(sqlalchemy.String, unique=True)
    listen_port = Column(sqlalchemy.String, unique=True)
    private_key = Column(sqlalchemy.String)
    public_key = Column(sqlalchemy.String)
    endpoint = Column(sqlalchemy.String)
    dns = Column(sqlalchemy.String)

    post_up = Column(sqlalchemy.String)
    post_down = Column(sqlalchemy.String)
    is_running = Column(sqlalchemy.Boolean)
    configuration = Column(sqlalchemy.Text)

    peers = relationship("WGPeer", cascade="all, delete", passive_deletes=True, lazy="joined")


class WGPeer(Base):
    __tablename__ = "peer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(sqlalchemy.String, default="Unnamed")
    address = Column(sqlalchemy.String)
    public_key = Column(sqlalchemy.String)
    private_key = Column(sqlalchemy.String)
    shared_key = Column(sqlalchemy.Text)
    dns = Column(sqlalchemy.Text)
    allowed_ips = Column(sqlalchemy.String)

    server_id = Column(Integer, sqlalchemy.ForeignKey('server.id', ondelete="CASCADE", onupdate="CASCADE"))
    server = relationship("WGServer", backref=backref("server"))
    configuration = Column(sqlalchemy.Text)
