from typing import Any
from .schema import Hash, Token, Payload, Header, Timestamp, Body, Duration
from .messages import ERROR_INVALID_TYPE
from pydantic import ValidationError
from time import time
from base64 import b64encode, b64decode
from hashlib import blake2b
from binascii import Error


def decode_signature(token: Token) -> Hash:
    """Takes a token and returns the signature.

    Args:
        token (Token): a `Token` object.

    Returns:
        Hash: a `Hash` object.
    """
    return token.signature


def header(
    duration: int = 60,
    type: str = "bootleg_jwt"
) -> Header:
    """builds the token header and returns the appropriate object.

    Args:
        duration (int, optional): _description_. Defaults to 60 seconds.
        type (str, optional): _description_. Defaults to "bootleg_jwt".

    Returns:
        Header: _description_. `pydantic.BaeModel` object representing the token header.
    """
    time = get_time()
    return Header(
        type=type,
        duration=Duration(value=duration),
        created=Timestamp(value=time),
        expires=Timestamp(value=time+duration)
    )


def body(
    user: Any,
    data: Any,
    model: Body = Body
):
    """Constructs a `body` model for the token.

    Args:
        user (Any): An object representing a user account.
        data (Any): An object representing some arbitrary data linked to the user account.
        model (BaseModel, optional): A `pydantic.BaseModel` object representing the body model. Allows this function to operate as a constructor for bodies with strictly defined `user` and `data` objects.

    Returns: constructed and validated body model.

    """
    return model(user=user,data=data)


def blake2bhash(
    data: bytes,
    secret_key: bytes = b'',
    person: bytes = b'',
    salt: bytes = b'',
) -> bytes:
    """hashlib.blake2b.

    Args:
        data (bytes): Data to be hashed.
        secret_key (bytes, optional): A secret key. Can be used to turn hashes into signatures. Defaults to empty.
        person (bytes, optional): A small bytestring used to namespace hashes. Defaults to empty.
        salt (bytes, optional): A small bytestring used to salt hashes. Defaults to empty.

    Returns:
        bytes: utf-8 encoded hex digest
    """
    return blake2b(data,key=secret_key,person=person,salt=salt).hexdigest().encode()


def decode_token(token: bytes) -> Token:
    """Takes a bytestring, does some validation on it, and if its a token, returns that token.
    Used in the validation process.


    Args:
        token (bytes): A base64 encoded bytestring representing a `Token` object.


    Returns:
        Token: `Token` object.
    """
    try:
        if not isinstance(token, bytes): raise TypeError(ERROR_INVALID_TYPE)
        token = b64decode(token)
        parsed = Token.parse_raw(token)
    except Error: return False
    except ValidationError: return False
    except TypeError: return False
    else: return parsed


def derive_payload(token: Token) -> Payload:
    """'reverse engineers' the payload from an arbitrary token. Used for validation.

    Args:
        token (Token): A token object.

    Returns:
        Payload: a payload object.
    """
    return Payload(
        header=token.header,
        body=token.body
    )


def encode_token(token: Token) -> Token:
    """Encode a `Token` object in base64. This is what is returned to the client.

    Args:
        token (Token): `Token` object.

    Returns:
        bytes: `Token.json().encode()` encoded in base64.
    """
    return b64encode(token.json().encode())


def encode_payload(payload: Payload) -> bytes:
    """Encode the payload for hashing. The hashed payload is used to create the `Signature` object appended to the `Header` and `Body` objects in the final returned bytestring. encode_payload() is used in the validation and generation process. This is crucial for ensuring the blake2b hash is reproducible.

    Args:
        payload (Payload): A pydantic object representing the `Header` and `Body` objects of a `Token`.

    Returns:
        bytes: the payload header and body, in json, encoded to bytestring, concactenated by a period, then encoded in base64.
    """
    return b64encode(payload.header.json().encode() + b'.' + payload.body.json().encode())


def sign_payload(
    payload: Payload,
    _secret: bytes,
    _salt=b'',
    _person=b'',
) -> Hash:
    signature = blake2bhash(
        data=encode_payload(payload),
        secret_key=_secret,
        person=_person,
        salt=_salt
    )
    keyed = True if _secret else False
    _salt = _salt
    _person = _person
    signature = Hash(value=signature,keyed=keyed,salt=_salt,person=_person)
    return signature


def get_time() -> int:
    """Return the current unix epoch.

    Returns:
        int: Current time in seconds since unix epoch (01/01/1970 at 00:00)
    """
    return int(time())