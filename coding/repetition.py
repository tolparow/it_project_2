from noize import iochannel as io


#Repetition algorithm by default 3
# TODO: do both tests for mult = 3 and mult = 5
def code(message, mult = 3):
    result = bytearray()

    for i in range(len(message) * mult):
        b1 = original[i]
        b2 = received[i]
        for bit in range(8):
            if (b1 & 1) != (b2 & 1):
                count += 1
            b1 >>= 1
            b2 >>= 1
    return count



bytes = io.get_bytes("input.txt", is_file=True)
print(bytes)
result = code(bytes)
io.write_file(result)
# def decode(message):
