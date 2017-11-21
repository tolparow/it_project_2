import datetime

from message_processing.compression.compression import compress, decompress, Compression, ext_algo_mapping as c_algs
from message_processing.encoding.encoding import encode, decode, Encoding, ext_algo_mapping as e_algs
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

    ext = 'txt' if text is not None else file_path.rsplit('.', 1)[-1]

    clear = None
    if text is not None:
        clear = bytes(text, 'utf-8')
    else:
        with open(file_path, 'rb') as f:
            clear = f.read()

    s = '{} {} {} {} '.format(ext, c_algs[ext].name, e_algs[ext].name,  len(clear))

    t = datetime.datetime.now().timestamp()
    compressed = compress(clear, ext)

    s += str(len(compressed)) + ' ' + str(datetime.datetime.now().timestamp() - t) + ' '
    t = datetime.datetime.now().timestamp()

    encoded = encode(compressed, ext)

    s += str(len(encoded)) + ' ' + str(datetime.datetime.now().timestamp() - t) + ' '
    t = datetime.datetime.now().timestamp()

    noisy = make_some_noise(encoded, noise_rate)

    s += str(datetime.datetime.now().timestamp() - t) + ' '
    t = datetime.datetime.now().timestamp()

    decoded = decode(noisy, ext)

    s += str(datetime.datetime.now().timestamp() - t) + ' '
    t = datetime.datetime.now().timestamp()

    decompressed = decompress(decoded, ext)

    s += str(datetime.datetime.now().timestamp() - t) + ' '

    print(s)

    return decompressed

#
# print(process_message(open(), noise_rate=0.05).decode('utf-8', errors='replace'))
#
# for i in range(1, 6):
#     file_name = 'datasets/BMP/Big/f' + str(i) + '.bmp'
#     process_message(None, file_path=file_name, noise_rate=0.00)
#
# for i in range(1, 6):
#     file_name = 'datasets/WAV/Big/f' + str(i) + '.wav'
#     process_message(None, file_path=file_name, noise_rate=0.00)
#
# for i in range(1, 6):
#     file_name = 'datasets/GIF/Big/f' + str(i) + '.gif'
#     process_message(None, file_path=file_name, noise_rate=0.00)
#
# for i in range(1, 6):
#     file_name = 'datasets/RTF/Big/f' + str(i) + '.rtf'
#     process_message(None, file_path=file_name, noise_rate=0.00)
#
# for i in range(1, 6):
#     file_name = 'datasets/TIF/Big/f' + str(i) + '.tif'
#     process_message(None, file_path=file_name, noise_rate=0.00)