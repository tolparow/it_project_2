from enum import Enum


class Encoding(Enum):
    REPETITION_3 = ('encoding/repetition.py', 3)
    REPETITION_5 = ('encoding/repetition.py', 5)
    GOLAY = ('encoding/golay.py', None)
    HAMMING = ('encoding/hamming.py', None)



class Compression(Enum):
    LZ78 = 'compression/lz78.py'
    HUFFMAN = 'huffman.py'
    SFE = 'compression/sfe.py'


def process_message(text: str, file_path: str = None, noise_rate: float = 0.0,
                    encoding: Encoding = None, compression: Compression = None):
    """
    Process message in such a way:
    compress -> encode -> 'send' by noisy channel -> decode -> decompress

    Method accepts either message text, or file_path exclusively.
    The returned message/file is processed fully, and, it might be damaged, if
    compression is lossy, or if the was some noise applied.

    :param text: text of the message in UTF-8 string
    :param file_path: file path if it is needed
    :param noise_rate: rate of noise applied in channel
    :param encoding: encoding algorithm enum
    :param compression: compression algorithm enum
    :return: text of processed message, if any, or address of processed file
    """

    assert (text is None) != (file_path is None), 'Provide either text, or file_path, not both!'
    assert 0.0 >= noise_rate >= 1.0, 'Noise rate should be in [0.0;1.0]!'


