import math
import os
import time

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
    """
        Bytes to bitstring (b'\x01' -> '0001')
        :param b: bytes
        :return: bitstring
    """
    s = ''.join(format(x, '08b') for x in b)
    return s


def pre_prepare_bits(bits):
    """
    this function is oposite of post_prepare_bits, and it's remove meaningless data
    :param bits: current bits
    :return: bits with removing meaningless data
    """
    try:
        while bits[0] == '0':
            bits = bits[1:]
    except Exception as e:
        print(e)
    bits = bits[1:]
    return bits


def post_prepare_bits(bits):
    """
        this function helps to make fully filled bytes
        :param bits: current bits
        :return: bits with adding 	meaningless data
        """
    bits = '1' + bits
    while len(bits) % 8 != 0:
        bits = '0' + bits
    return bits


class Hamming:
    def covers(self, i, j):
        """
        Checks that bit j belongs to parity i
        :return: True/False
        """
        return (j >> int(math.log(i, 2))) % 2 == 1

    def sum_bits(self, bits, i):
        """
        :param bits: current bits sequence
        :param i: current parity
        :return:  sum of bits that belongs to parity i
        """
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
        """
        :param bits: bits sequence
        :return: integer for this bits
        """
        if bits == []:
            return 0
        else:
            n = bits[0] * (2 ** (len(bits) - 1))
            return n + self.bits_to_number(bits[1:])

    def prepare(self, bits):
        """
        :param bits: current bits sequence
        :return: bits sequence with adding free positions for parity bits
        """
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
        """
        This function calculates the values of parity bits in current sequene
        :param bits: current bits seuquence
        :return: sequence of bits with calculated parity bits
        """
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
        """
        This function encodes the data by hamming code.
        :param message: Data that this function need to encode
        :param is_string:
        :return:encoded data
        """
        bits = ""
        if is_string:
            bits = bytes_to_bitstring(message)
        else:
            bits = message[:]
        result = ""
        for i in range(0, len(bits), 8):
            cur_bits = ""
            for j in range(8):
                if i + j < len(bits):
                    cur_bits += bits[i + j]
            bits_with_paraties = self.prepare(cur_bits)
            result += self.set_parity_bits(bits_with_paraties)
        return bitstring_to_bytes(post_prepare_bits(result))

    def decode(self, message, is_string=True):
        """
        This function decodes the data that was encoded by Hamming code
        :param message: Data to be encoded
        :param is_string:
        :return: encoded data
        """
        bits = ""
        if is_string:
            bits = bytes_to_bitstring(message)
        else:
            bits = message[:]
        result = ""
        bits = pre_prepare_bits(bits)
        for i in range(0, len(bits), 12):
            cur_bits = ""
            for j in range(12):
                if i + j < len(bits):
                    cur_bits += bits[i + j]
            parity_results = self.check_parity(cur_bits, power_2_below(len(cur_bits)))
            n = self.bits_to_number(parity_results)
            if n != 0:
                cur_bits[n - 1] = 1 - cur_bits[n - 1]
            result += self.extract_data(cur_bits)
        return bitstring_to_bytes(result)

    def extract_data(self, bits):
        """
        Extracting data for bits sequence
        by removing parity bits from sequence
        :param bits: current bits sequence
        :return: Result of extracted data
        """
        result = ""
        for i in range(1, len(bits) + 1):
            if not is_power_of_two(i):
                result += bits[i - 1]
        return result

    def check_parity(self, bits, i):
        """
        This recursive function checks the result of parity bits
        :param bits: cur bits sequence
        :param i: index of current bit in bits sequence
        :return:  returns sum of positions of all incorrect parity bits in this sequence
        """
        if i == 1:
            return [0] if self.has_odd_parity(bits, i) else [1]
        else:
            bit = 0 if self.has_odd_parity(bits, i) else 1
            return [bit] + self.check_parity(bits, power_2_below(i - 1))
