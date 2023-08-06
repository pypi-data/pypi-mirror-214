from .schema import Token, Payload
from .funcs import encode_token, decode_token, derive_payload, sign_payload, get_time, header
from .messages import *
from decouple import config, UndefinedValueError


"""
Explaining the _secret, _salt, and _person arguments:


_secret is defined by the `local environment`. This should be a \\secret\\. No matter \\what\\. This can rotate, and it can be shared... but it must be shared securely between machines (i.e. with some sort of conainer orchestration tool, or proxmox.... something....)


_salt and _person are a salt and namespace respectively. Implement these to allow fine control over tokens. For example: A salt could be implemented, then stored in a database. When a token is renewed, the salt and namespace should be derived from the token. When a token is \\first generated\\, the \\salt and namespace are generated\\. Any time a token is \\renewed\\, the \\salt and namespace are derived\\.
"""


class BootlegJWT():
    """Generates a new token if provided with a payload. Validates an existing token if provided with a token.

    Args:
        payload (Payload): Provide `BootlegJWT` with a `payload` to generate a new token. The `payload` is a pydantic object provided by `bootleg_jwt.Payload`. This object is first hashed, then the hash is put into a `bootleg_jwt.schema.Signature` object and appended to the payload.

        token (Token): Provided with a `token`, `BootlegJWT` will validate the token and return a `BootlegJWT` object with `BootlegJWT.VALID = True`
    """
    VALID: bool = False
    TOKEN: Token = False
    ENCODED: bytes = False
    DECODED: Token = False
    JSON: Token.json = False


    def __init__(
        self,
        token: bytes = False,
        payload: Payload = False,
        insecure_mode = False,
        **kwargs
    ):
        try: _secret = config('SECRET').encode()
        except UndefinedValueError:
            if not insecure_mode and not token:
                print("WARNING: Secret has not been set. The resultant token will not be keyed, and therefore, will be replicable by anybody with `BootlegJWT`. To quiet this warning, use `insecure_mode = True` when instantiating `BootlegJWT`.")
            _secret = b''
        if not token and not payload: raise Exception(ERROR_INVALID_USE)
        if token and payload: raise Exception(ERROR_INVALID_USE)
        if payload: self.generate(payload, _secret, **kwargs)
        if token: token = decode_token(token)
        if token: self.validate(token, _secret)


    def generate(
        self,
        payload: Payload,
        _secret: bytes = b'',
        **kwargs
    ):
        _salt: bytes = b''
        _person: bytes = b''
        for i in kwargs.keys():
            if i == '_salt': _salt = kwargs[i].encode()[0:15] if not isinstance(kwargs[i],bytes) else kwargs[i]
            if i == '_person': _person = kwargs[i].encode()[0:15] if not isinstance(kwargs[i],bytes) else kwargs[i]
        signature = sign_payload(payload, _secret, _salt=_salt, _person=_person)
        _token: Token = Token(header=payload.header,body=payload.body,signature=signature)
        self.TOKEN = _token
        self.DECODED = _token
        self.JSON = _token.json(indent=4)
        self.ENCODED = encode_token(_token)
        valid = self.validate(_token,_secret)
        if valid: self.VALID = True


    def validate(
        self,
        token: Token,
        _secret: bytes = b''
    ):
        _salt = b''
        _person = b''
        is_valid = False
        expired = True if get_time() > token.header.expires.value else False
        if expired: return False
        payload = derive_payload(token)
        token_signature = token.signature.value
        if token.signature.salt: _salt = token.signature.salt
        if token.signature.person: _person = token.signature.person
        signature = sign_payload(payload, _secret,_salt=_salt,_person=_person)
        payload_signature = signature.value
        if token_signature.decode() == payload_signature.decode(): is_valid = True
        if is_valid:
            self.VALID = True
            self.TOKEN = token
            self.DECODED = token
            self.JSON = token.json(indent=4)



async def renew(token: bytes) -> BootlegJWT:
    """Validates a token and returns a new one with a new expiration date. Retains all of the original token's characteristics.

    Args:
        token (bytes): the token to be validated, and then renewed.


    Returns:
        BootlegJWT: Returns an instance of `BootlegJWT` to be used as noemal.
    """
    _salt = b''
    _person = b''
    validate = BootlegJWT(token)
    if not validate.VALID: raise Exception("Invalid token.")
    if validate.DECODED.signature.salt: _salt = validate.DECODED.signature.salt
    if validate.DECODED.signature.person: _person = validate.DECODED.signature.person
    payload = Payload(
        header = header(duration=validate.DECODED.header.duration.value,type=validate.DECODED.header.type),
        body = validate.DECODED.body
    )
    new = BootlegJWT(payload=payload,_salt=_salt,_person=_person)
    return new



