#Repetition algorithm by default 3
# TODO: do both tests for mult = 3 and mult = 5
#returns coded bytes
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
    return bitstring_to_bytes(result)



def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

#returns encoded bytes
def encode(message, mult = 3, is_string=True):
    bits = ''
    bytes = bytearray()
    if is_string:
        bytes = bytearray(message, 'utf8')
    else:
        bytes = message[:]

    for st in bytes:
        tmp = bin(st)[2:]
        bits += '0' * (8 - len(tmp)) + tmp
    result = ''
    for i in range(0, len(bits), mult):
        count = 0
        for oft in range(mult):
            if bits[i + oft] == '1':
                count += 1
        if count > mult / 2:
            result += '1'
        else:
            result += '0'
    return bitstring_to_bytes(result)



# kek = code("kek")
# # print(kek)
#
# decoded = encode(kek, is_string=False)
# print(decoded)


# bytes = io.get_bytes("input.txt", is_file=True)
# print(bytes)
# result = code(bytes)
# io.write_file(result)
# # def decode(message):
