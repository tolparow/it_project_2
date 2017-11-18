import math
import os


def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


def is_power_of_two(n):
    return n & (n - 1) == 0


def power_2_below(n):
    return 2 ** int(math.log(n, 2))


def bytes_to_bitstring(b):
    s = ''.join(format(x, '08b') for x in b)
    return s


def pre_prepare_bits(bits):
    leng = len(bits)
    try:
        while bits[0] == '0':
            bits = bits[1:]
    except Exception as e:
        print(e)
    bits = bits[1:]
    return bits


def post_prepare_bits(bits):
    leng = len(bits)
    bits = '1' + bits
    while len(bits) % 8 != 0:
        bits = '0' + bits
    return bits


class Hamming:
    def covers(self, i, j):
        return (j >> int(math.log(i, 2))) % 2 == 1

    def sum_bits(self, bits, i):
        if i > len(bits):
            return 0
        else:
            result = 0
            for j in range(i, len(bits) + 1):
                if self.covers(i, j):
                    result += int(bits[j - 1])
            return result

    def has_odd_parity(self, bits, i):
        return self.sum_bits(bits, i) % 2 == 1

    def has_even_parity(self, bits, i):
        return self.sum_bits(bits, i) % 2 == 0

    def bits_to_number(self, bits):
        if bits == []:
            return 0
        else:
            n = bits[0] * (2 ** (len(bits) - 1))
            return n + self.bits_to_number(bits[1:])

    def prepare(self, bits):
        result = ""
        j = 0
        i = 0
        while i < len(bits):
            if is_power_of_two(i + j + 1):
                result += '0'
                j += 1
                i -= 1
            else:
                result += bits[i]
            i += 1
        return result

    def set_parity_bits(self, bits):
        for i in range(1, len(bits) + 1):
            if is_power_of_two(i):
                if self.has_odd_parity(bits, i):
                    if bits[i - 1] != '0':
                        bits = bits[:i - 1] + '0' + bits[i:]
                else:
                    if bits[i - 1] != '1':
                        bits = bits[:i - 1] + '1' + bits[i:]
        return bits

    def encode(self, message, is_string=True):
        bits = ""
        if is_string:
            bits = bytes_to_bitstring(message)
        else:
            bits = message[:]
        bits_with_paraties = self.prepare(bits)
        return bitstring_to_bytes(post_prepare_bits(self.set_parity_bits(bits_with_paraties)))

    def decode(self, message, is_string=True):
        bits = ""
        if is_string:
            bits = bytes_to_bitstring(message)
        else:
            bits = message[:]
        bits = pre_prepare_bits(bits)
        parity_results = self.check_parity(bits, power_2_below(len(bits)))
        n = self.bits_to_number(parity_results)

        if n != 0:
            print
            "NB: bit ", n, " is bad. Flipping."
            bits[n - 1] = 1 - bits[n - 1]

        return bitstring_to_bytes(self.extract_data(bits))

    def extract_data(self, bits):
        result = ""
        for i in range(1, len(bits) + 1):
            if not is_power_of_two(i):
                result += bits[i - 1]
        return result

    def check_parity(self, bits, i):
        if i == 1:
            return [0] if self.has_odd_parity(bits, i) else [1]
        else:
            bit = 0 if self.has_odd_parity(bits, i) else 1
            return [bit] + self.check_parity(bits, power_2_below(i - 1))


def compress(path=None, to_be_compressed=None):
    if path is not None:
        with open(path, 'rb') as f:
            text = f.read()
        h = Hamming()
        compressed = h.encode(text)
        filename, file_extension = os.path.splitext(path)
        output_path = filename + ".hamm"
        with open(output_path, 'wb') as output:
            output.write(compressed)
        return output_path
    else:
        h = Hamming()
        return h.compress(to_be_compressed)


def decompress(path=None, extension=None, compressed=None):
    if path is not None:
        with open(path, 'rb') as f:
            text = f.read()
        h = Hamming()
        decompressed = h.decode(text)
        filename, file_extension = os.path.splitext(path)
        output_path = filename + "_decompressed" + extension
        with open(output_path, 'wb') as output:
            output.write(decompressed)
        return output_path
    else:
        h = Hamming()
        return h.decode(compressed)
