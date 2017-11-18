from message_processing.message_processor import Compression
from . import huffman
from enum import Enum

ext_algo_mapping = {
    'aiff': Compression.HUFFMAN,
    'tiff': Compression.HUFFMAN,
    'bmp': Compression.HUFFMAN,
    'gif': Compression.HUFFMAN,
    'rtf': Compression.HUFFMAN,
    'txt': Compression.HUFFMAN,
    'wav': Compression.HUFFMAN,
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
    # TODO add more algos when merged
    else:
        return None


def compress(text: str, file_path: str = None, compression: Compression = None):
    """

    :param text:
    :param file_path:
    :return:
    """

    assert (text is None) != (file_path is None), 'Provide either text, or file_path, not both!'

    ext = 'txt' if text is not None else file_path.rsplit('.', 1)[1]

    algo = get_algo_module(ext)

    algo.compress(text, file_path)
