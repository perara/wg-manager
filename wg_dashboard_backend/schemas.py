import pydantic
from pydantic import BaseModel, typing
from sqlalchemy.orm import Session, Query
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import logging
import models

_LOGGER = logging.getLogger(__name__)


class GenericModel(BaseModel):

    class Meta:
        model = None
        key = None
        excludes = {"id"}

    class Config:
        orm_mode = True

    def _ensure_orm(self):
        if not self.Config and not self.Config.orm_mode and not self.Meta.model and not self.Meta.key:
            raise NotImplementedError("Incorrect configuration Config.orm_mode must be enabled and Meta.model must be "
                                      "set to a sqlalchemy model. Additional Meta.key must be set to bind model and schema")

    def filter_query(self, sess) -> Query:
        query = sess.query(self.Meta.model).filter_by(**{
            self.Meta.key: getattr(self, self.Meta.key)
        })

        return query

    def update(self, sess: Session, new):
        self._ensure_orm()

        self.filter_query(sess).update(new.dict(include=self.columns()))

        sess.commit()

        for k, v in new.dict().items():
            try:
                setattr(self, k, v)
            except ValueError:
                pass

        return self

    def columns(self, no_exclude=False):
        cols = set([x for x in dir(self.Meta.model) if not x.startswith("_")])
        #cols = set([str(x).replace(f"{self.Meta.model.__table__.name}.", "") for x in self.Meta.model.__table__.columns])
        return cols if no_exclude else cols - self.Meta.excludes

    def sync(self, sess: Session):
        self._ensure_orm()

        # Count existing
        n_results = self.filter_query(sess).count()
        if n_results == 0:
            # Insert, does not exists at all.
            # Convert from schema to model
            dbm = self.Meta.model(**self.dict())
            sess.add(dbm)
        else:
            self.filter_query(sess).update(self.dict(include=self.columns()))

        sess.commit()

    def from_db(self, sess: Session):
        self._ensure_orm()

        try:
            db_item = self.filter_query(sess).one()

            for c in self.columns(no_exclude=True):
                try:
                    setattr(self, c, getattr(db_item, c))
                except ValueError as e:
                    pass
            return self
        except MultipleResultsFound as e:
            _LOGGER.exception(e)
        except NoResultFound as e:
            _LOGGER.exception(e)

        _LOGGER.warning("We did not find any records in the database that corresponds to the model. This means you "
                        "are trying to fetch a unsaved schema!")
        return None


class User(GenericModel):
    id: int = None
    username: str
    email: str = None
    full_name: str = None
    role: str = None

    class Meta:
        model = models.User
        key = "username"
        excludes = {"id"}


class UserInDB(User):
    password: str


class Token(GenericModel):
    access_token: str
    token_type: str
    user: User


class WGPeer(GenericModel):
    id: int = None
    name: str = None
    address: str = None
    private_key: str = None
    public_key: str = None
    shared_key: str = None
    server_id: str
    dns: str = None
    allowed_ips: str = None
    configuration: str = None

    class Meta:
        model = models.WGPeer
        key = "address"
        excludes = {"id"}


class WGPeerConfig(GenericModel):
    config: str


class KeyPair(GenericModel):
    public_key: str
    private_key: str


class PSK(GenericModel):
    psk: str


class WGServer(GenericModel):
    id: int = None
    address: str = None
    interface: str
    listen_port: int = None
    endpoint: str = None
    private_key: str = None
    public_key: str = None
    is_running: bool = None
    configuration: str = None
    post_up: str = None
    post_down: str = None
    dns: str = None

    peers: pydantic.typing.List['WGPeer'] = []

    class Meta:
        model = models.WGServer
        key = "interface"
        excludes = {"id", "peers"}

    def convert(self):
        self.peers = [] if not self.peers else self.peers
        return models.WGServer(**self.dict(exclude={"is_running"}))


class WGServerAdd(WGServer):
    address: str
    interface: str
    listen_port: int


class WGPeerAdd(GenericModel):
    server_interface: str

