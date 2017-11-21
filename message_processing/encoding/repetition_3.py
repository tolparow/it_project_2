from . import repetition


def encode(to_encode: bytes):
    return repetition.encode(to_encode, 3)


def decode(to_decode: bytes):
    return repetition.decode(to_decode, 3)
