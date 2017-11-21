from enum import Enum

from . import golay, hamming, repetition_3, repetition_5


class Encoding(Enum):
    REPETITION_3 = ('encoding/repetition.py', 3)
    REPETITION_5 = ('encoding/repetition.py', 5)
    GOLAY = ('encoding/golay.py', None)
    HAMMING = ('encoding/hamming.py', None)


ext_algo_mapping = {
    'aiff': Encoding.REPETITION_3,
    'tif': Encoding.REPETITION_3,
    'bmp': Encoding.REPETITION_3,
    'gif': Encoding.REPETITION_3,
    'rtf': Encoding.REPETITION_3,
    'txt': Encoding.REPETITION_5,
    'wav': Encoding.REPETITION_3,
}


def get_algo_module(file_ext: str = None):
    # TODO finish comments
    """

    :param file_ext:
    :param encoding:
    :return:
    """
    if file_ext is None or file_ext.lower() not in ext_algo_mapping:
        algo = ext_algo_mapping['txt']
    else:
        algo = ext_algo_mapping[file_ext.lower()]

    if algo == Encoding.REPETITION_3:
        return repetition_3
    elif algo == Encoding.REPETITION_5:
        return repetition_5
    elif algo == Encoding.GOLAY:
        return golay
    elif algo == Encoding.HAMMING:
        return hamming
    else:
        raise AttributeError()


def encode(to_encode: bytes, ext: str):
    """

    :param to_encode:
    :param ext:
    :return:
    """

    return get_algo_module(ext).encode(to_encode)


def decode(to_decode: bytes, ext: str):
    """

    :param to_decode:
    :param ext:
    :return:
    """

    return get_algo_module(ext).decode(to_decode)
