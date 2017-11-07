from noize import iochannel as io
from bitarray import bitarray
import binascii

#Repetition algorithm by default 3
# TODO: do both tests for mult = 3 and mult = 5
def code(message, mult = 3, is_string=True):
    bits = ""
    bytes = bytearray()
    if is_string:
        bytes = bytearray(message, 'utf8')
    else:
        bytes = message[:]

    for st in bytes:
        tmp = bin(st)[2:]
        bits += '0' * (8-len(tmp)) + tmp

    result = ""
    for bit in bits:
        for i in range(mult):
            result += bit
    print(len(result))
    return bitstring_to_bytes(result)



def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

# def encode(message, mult=3):


kek = code("kek")
print(kek)
io.write_file(kek)


# bytes = io.get_bytes("input.txt", is_file=True)
# print(bytes)
# result = code(bytes)
# io.write_file(result)
# # def decode(message):
