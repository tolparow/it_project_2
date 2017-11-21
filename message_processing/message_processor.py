from message_processing.compression.compression import *
from message_processing.encoding.encoding import *
from message_processing.noise import make_some_noise


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
    #    assert 0.0 >= noise_rate >= 1.0, 'Noise rate should be in [0.0;1.0]!'

    ext = 'txt' if text is not None else file_path.rsplit(1)[-1]

    clear = None
    if text is not None:
        clear = bytes(text, 'utf-8')
    else:
        with open(file_path, 'rb') as f:
            clear = f.read()

    compressed = compress(clear, ext)

    encoded = encode(compressed, ext)

    noisy = make_some_noise(encoded, noise_rate)

    decoded = decode(noisy, ext)

    decompressed = decompress(decoded, ext)

    return decompressed


# print(process_message('проверка!', noise_rate=0.5))
