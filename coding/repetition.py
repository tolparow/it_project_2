from bitarray import bitarray


def code(message: bytes, mult=3):
    """
    TODO: do both tests for mult = 3 and mult = 5

    :param message: input sequence
    :param mult: number of repetitions, 3 by default
    :return: coded bytes
    """
    bits = ""
    bytes = bytearray(message)

    for st in bytes:
        tmp = bin(st)[2:]
        bits += '0' * (8 - len(tmp)) + tmp

    result = ""
    for bit in bits:
        for i in range(mult):
            result += bit

    return __bitstring_to_bytes(result)


def encode(message: bytes, mult=3):
    """
    :param message: input sequence
    :param mult: number of repetitions
    :return: decoded message
    """
    bits = []
    bytes = bytearray(message)

    # Square asymptotic
    for st in bytes:
        tmp = bin(st)[2:]
        bits.append('0' * (8 - len(tmp)) + tmp)
    bits = ''.join(bits)
    result = ''
    # print(len(bits))
    for i in range(0, len(bits), mult):
        count = 0
        for oft in range(mult):
            if bits[i + oft] == '1':
                count += 1
        if count > mult / 2:
            result += '1'
        else:
            result += '0'
    return __bitstring_to_bytes(result)


def __bitstring_to_bytes(s):
    return bitarray(s).tobytes()
