from bitarray import bitarray


def encode(message: bytes, mult=3):
    """
    TODO: do both tests for mult = 3 and mult = 5

    :param message: input sequence
    :param mult: number of repetitions, 3 by default
    :return: coded bytes
    """
    bits = []
    bytes = bytearray(message)

    for st in bytes:
        tmp = bin(st)[2:]
        bits.append('0' * (8 - len(tmp)) + tmp)

    bits = ''.join(bits)
    result = []
    for bit in bits:
        result.append(bit * mult)

    return __bitstring_to_bytes(''.join(result))


def decode(message: bytes, mult=3):
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
    result = []
    # print(len(bits))
    count, i = 0, 0
    for bit in bits:
        if i % mult == 0 and i != 0:
            if count > mult / 2:
                result.append('1')
            else:
                result.append('0')
            count = 0

        if bit == '1':
            count += 1
        i += 1
    if count > mult / 2:
        result.append('1')
    else:
        result.append('0')

    # for i in range(0, len(bits), mult):
    #     count = 0
    #     for oft in range(mult):
    #         if bits[i + oft] == '1':
    #             count += 1
    #     if count > mult / 2:
    #         result.append('1')
    #     else:
    #         result.append('0')
    return __bitstring_to_bytes(''.join(result))


def __bitstring_to_bytes(s):
    return bitarray(s).tobytes()
