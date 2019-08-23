import binascii
from base64 import b32encode, b32decode


class NonDehumanizableId(Exception):
    pass


def dehumanize(humanized_id: str) -> int:
    if humanized_id is None:
        return None
    missing_padding = len(humanized_id) % 8
    if missing_padding != 0:
        humanized_id += '=' * (8 - missing_padding)
    try:
        xbytes = b32decode(humanized_id.replace('8', 'O').replace('9', 'I'))
    except binascii.Error:
        raise NonDehumanizableId('id non dehumanizable')
    return int_from_bytes(xbytes)


def humanize(technical_id: int) -> str:
    if technical_id is None:
        return None
    b32 = b32encode(int_to_bytes(technical_id))
    return b32.decode('ascii') \
        .replace('O', '8') \
        .replace('I', '9') \
        .rstrip('=')


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')
