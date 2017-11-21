from enum import Enum

from . import huffman, lz78, shannon_fano


class Compression(Enum):
    LZ78 = 'compression/lz78.py'
    HUFFMAN = 'huffman.py'
    SF = 'compression/sfe.py'


ext_algo_mapping = {
    'aiff': Compression.SF,
    'tif': Compression.SF,
    'bmp': Compression.SF,
    'gif': Compression.SF,
    'rtf': Compression.SF,
    'txt': Compression.SF,
    'wav': Compression.SF,
}


def get_algo_module(file_ext: str = None, compression: Compression = None):
    # TODO finish comments
    """

    :param information_type:
    :param compression:
    :return:
    """
    if file_ext is None or file_ext.lower() not in ext_algo_mapping:
        algo = ext_algo_mapping['txt']
    else:
        algo = ext_algo_mapping[file_ext.lower()]

    if algo == Compression.HUFFMAN:
        return huffman
    elif algo == Compression.LZ78:
        return lz78
    elif algo == Compression.SF:
        return shannon_fano
    else:
        raise AttributeError()


def compress(to_compress: bytes, ext: str):
    """

    :param text:
    :param file_path:
    :return:
    """

    assert to_compress is not None, 'Provide bytes to compress!'

    return get_algo_module(ext).compress(to_compress)


def decompress(to_decompress: bytes, ext: str):
    """

    :param text:
    :param file_path:
    :return:
    """

    assert to_decompress is not None, 'Provide bytes to compress!'

    return get_algo_module(ext).decompress(to_decompress)
