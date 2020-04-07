from pydantic import BaseModel, typing

import models


class User(BaseModel):
    username: str = None
    email: str = None
    full_name: str = None
    role: str = None

    class Config:
        orm_mode = True


class UserInDB(User):
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

    class Config:
        orm_mode = True


class WGPeer(BaseModel):
    name: str = None
    address: str = None
    private_key: str = None
    public_key: str = None
    server: str
    dns: str = None
    allowed_ips: str = None
    # TODO missing stuff

    class Config:
        orm_mode = True


class WGPeerConfig(BaseModel):
    config: str


class KeyPair(BaseModel):
    public_key: str
    private_key: str


class PSK(BaseModel):
    psk: str


class WGServer(BaseModel):
    address: str = None
    interface: str
    listen_port: int = None
    endpoint: str = None
    private_key: str = None
    public_key: str = None
    shared_key: str = None
    is_running: bool = None

    post_up: str = None
    post_down: str = None

    peers: typing.List[WGPeer] = None

    class Config:
        orm_mode = True

    def convert(self):
        self.peers = [] if not self.peers else self.peers
        return models.WGServer(**self.dict(exclude={"is_running"}))


