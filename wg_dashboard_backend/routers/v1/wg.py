from fastapi import APIRouter

import middleware
import schemas
import script.wireguard

router = APIRouter()


@router.get("/generate_psk", response_model=schemas.PSK)
def generate_psk():
    return schemas.PSK(
        psk=script.wireguard.generate_psk()
    )


@router.get("/generate_keypair", response_model=schemas.KeyPair)
def generate_key_pair():
    keys = script.wireguard.generate_keys()
    private_key = keys["private_key"]
    public_key = keys["public_key"]
    return schemas.KeyPair(
        private_key=private_key,
        public_key=public_key
    )
