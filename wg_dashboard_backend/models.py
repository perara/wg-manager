import sqlalchemy
from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(sqlalchemy.String, unique=True, index=True)
    password = Column(sqlalchemy.String)
    username = Column(sqlalchemy.String, unique=True)
    full_name = Column(sqlalchemy.String)
    role = Column(sqlalchemy.String)


class WGPeer(Base):
    __tablename__ = "peer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(sqlalchemy.String, default="Unnamed")
    address = Column(sqlalchemy.String)
    public_key = Column(sqlalchemy.String)
    private_key = Column(sqlalchemy.String)
    dns = Column(sqlalchemy.String)
    allowed_ips = Column(sqlalchemy.String)

    server = Column(Integer, sqlalchemy.ForeignKey('server.interface'))
    server_ref = relationship("WGServer", backref="server")


class WGServer(Base):
    __tablename__ = "server"

    id = Column(Integer, primary_key=True, index=True)
    interface = Column(sqlalchemy.String, unique=True, index=True)
    address = Column(sqlalchemy.String, unique=True)
    listen_port = Column(sqlalchemy.String, unique=True)
    private_key = Column(sqlalchemy.String)
    public_key = Column(sqlalchemy.String)
    shared_key = Column(sqlalchemy.String)
    endpoint = Column(sqlalchemy.String)

    post_up = Column(sqlalchemy.String)
    post_down = Column(sqlalchemy.String)

    is_running = Column(sqlalchemy.Boolean)

    peers = relationship("WGPeer", backref="peer")
