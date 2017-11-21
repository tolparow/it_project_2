import rlp
import heapq
import os

from datetime import datetime
from rlp.codec import consume_item


def decode_rlp(d):
    """
    Decodes rlp string.
    Can decode even if string has redundant
    bytes to the right.
    :param d: bytes to be decoded
    :return: decoded instance
    """
    _, end = consume_item(d, 0)
    return rlp.decode(d[:end]), end


def bitstring_to_bytes(s):
    """
    String of bits to bytes ('0001' -> b'\x01')
    :param s: bitstring
    :return: bytes
    """
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')


def bytes_to_bitstring(b):
    """
    Bytes to bitstring (b'\x01' -> '0001')
    :param b: bytes
    :return: bitstring
    """
    s = ''.join(format(x, '08b') for x in b)
    return s


def compress(to_be_compressed=None):
    """
    Compress some file by its path, or
    UTF-8 string, or bytes.
    :param to_be_compressed: bytes or UTF-8 string to be compressed output in bytes
    :return: bytes of encoded what to_be_compressed
    """
    h = Huffman()
    return h.compress(to_be_compressed)


def decompress(compressed=None):
    """
    Decompress some file by its path, or
    UTF-8 string, or bytes.
    :param compressed: bytes to be decompressed in bytes or UTF-8 string
    :return: path of output file, or bytes of encoded string or bytes
    """
    h = Huffman()
    return decompress_bytes(compressed)


class HeapNode:
    """
    Heap node class.
    """

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class Huffman:
    """
    Main class for Huffman realization.
    """

    def __init__(self):
        self.tree = []
        self.codes = {}
        self.keys = {}

    @staticmethod
    def make_frequency_dict(text):
        """
        Build a frequency dict.
        :param text: text from which to build freq. dictionary
        :return: frequency dict. (e. g. {'A':10, 'B':5, etc.}
        """
        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def create_tree(self, frequency):
        """
        Create a heap depending on frequency
        :param frequency: a frequency dictionary
        :return:
        """
        for key in frequency:
            node = HeapNode(key, frequency[key])
            heapq.heappush(self.tree, node)

    def sum_nodes(self):
        """
        Sum least frequencies from heap, deleting from from the heap and putting result into the heap
        :return:
        """
        while len(self.tree) > 1:
            node1 = heapq.heappop(self.tree)
            node2 = heapq.heappop(self.tree)
            summed = HeapNode(None, node1.freq + node2.freq)
            summed.left = node1
            summed.right = node2
            heapq.heappush(self.tree, summed)

    def codes_giving(self, root, current_code):
        """
        Assigning codes going down the tree and giving left child 0 code and right child 1 code
        :param root: current position in tree
        :param current_code: current code assigned from the top going down to this node
        :return:
        """
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.keys[current_code] = root.char
            return

        self.codes_giving(root.left, current_code + "0")
        self.codes_giving(root.right, current_code + "1")

    def create_codes(self):
        """
        Create an empty string and start assigning codes
        :return:
        """
        root = heapq.heappop(self.tree)
        current_code = ""
        self.codes_giving(root, current_code)

    def get_encoded_text(self, text):
        """
        Instead letters assigning codes
        :param text: text from input file
        :return: encoded text
        """
        encoded = []
        for character in text:
            encoded.append(self.codes[character])
        return ''.join(encoded)

    def compress(self, text):
        """
        Compress UTF-8 text or bytes.
        :param text: text to be compressed
        :return: compressed bytes
        """
        frequency = Huffman.make_frequency_dict(text)
        self.create_tree(frequency)
        self.sum_nodes()
        self.create_codes()

        encoded_text = self.get_encoded_text(text)
        codes_list, codes, codes_mask = self.codes.values(), '', ''

        # Saving codewords and mask to the bytes
        # Mask is used to separate codes while decompressing
        # It saves the space - codes need only 2 * sum(len(codes)) bits to be stored
        for code in codes_list:
            codes += code
            codes_mask += '1' + '0' * (len(code) - 1)
        codes = codes_mask + codes

        # Symbols corresponded to codes are stored in list and serialized
        # using rlp algorithm. The last element of the list is the length of
        # codes and their mask which are written after symbols list.
        # This length helps to read all codes correctly.
        symbols = rlp.encode([x for x in self.codes.keys()] + [len(codes)])

        # Padding is used to fill encoded bits with some extension
        # to make its length to be multiple of 8.
        # The padding is n-1 zeroes and 1 one bits. E. g. if we need
        # to extend the string on 4 bits padding will be like 0001.
        # This makes easy to decompress - significant bits are read after fist 1.
        padding_length = 8 - len(codes + encoded_text) % 8
        padding = '' if padding_length == 0 else '0' * (padding_length - 1) + '1'

        # Concatenate all like this: symbols rlp bytes, codes and their mask, padding, encoded text
        return symbols + bitstring_to_bytes(codes + padding + encoded_text)


def decompress_bytes(compressed_bytes):
    """
    Decompress bytes that were previously compressed using compress function.
    :param compressed_bytes: compressed sequence of bytes
    :return: decompressed bytes
    """

    # Getting symbols stored and number of bits
    # used to store them.
    symbols, end = decode_rlp(compressed_bytes)

    # Get the lengths of codes and mask
    codes_len = int.from_bytes(symbols[-1], 'big')

    # Clean symbols list from last element and get bitstring to decode.
    symbols, bits = symbols[:-1], bytes_to_bitstring(compressed_bytes[end:])

    # Separate codes and mask from encoded bits
    codes = bits[:codes_len]
    encoded_bits = bits[bits.index('1', codes_len) + 1:]

    # Calculate dictionary which is going to be used to decode bitstring.
    # It looks like {'0': 'A', '10': 'B', '11': 'C'}.
    codes_to_symbols = {}
    code, k, mid = '', 0, len(codes) // 2
    for i in range(mid):
        if codes[i] == '0':
            code += codes[i + mid]
        else:
            if code != '':
                codes_to_symbols[code] = symbols[k]
                k += 1
            code = codes[i + mid]
    codes_to_symbols[code] = symbols[k]

    # Decompress the encoded  bitstring, reading it bit by bit.
    current_code, decoded_text = '', bytearray()
    for bit in encoded_bits:
        current_code += bit
        if current_code in codes_to_symbols:
            character = codes_to_symbols[current_code]
            decoded_text.append(int.from_bytes(character, 'big'))
            current_code = ''
    return decoded_text
