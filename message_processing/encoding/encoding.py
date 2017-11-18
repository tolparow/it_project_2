from message_processing.message_processor import Encoding
import importlib

def encode(text: str, file_path: str = None, encoding: Encoding = None):
    """

    :param text:
    :param file_path:
    :return:
    """
    algo = importlib.import_module(encoding)
    print(algo)


encode('1', encoding=Encoding.GOLAY)