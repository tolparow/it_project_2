import random

def get_bytes(obj, is_file=False):
    if is_file:
        with open(obj, 'rb') as f:
            return f.read()
    assert isinstance(obj, str), 'The object is neither string nor file path!'
    return bytes(obj, 'utf-8')


def get_str(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def make_some_noise(bytes, noise_level = 0.0, is_string=False):
    assert(noise_level >= 0 and noise_level <= 1), ("Wrong value of noise_level! " + str(noise_level) + " not in [0;1]  ")
    set_of_bytes = bytearray()
    if is_string:
        set_of_bytes = bytearray(bytes, 'utf-8')
    else:
        set_of_bytes = bytearray(bytes)

    for index, byte in enumerate(set_of_bytes):  #for every byte
        tmp = 0
        b = byte
        for i in range(8): #for every bit
            tmp >>= 1
            if random.random() < noise_level:
                #reverse
                tmp += 128 * (1 - b & 1)
            else:
                #save like in input
                tmp += 128 * (b & 1)
            b >>= 1
        set_of_bytes[index] = tmp
    return set_of_bytes

def write_to_file(content, file_name = "output.txt", is_string = False):
    if is_string:
        with open(file_name, 'w') as f:
            f.write(content)
    else:
        with open(file_name, 'wb') as f:
            f.write(content)


def write_bytes_with_noise(bytes, file_name = "output.txt", noise_level = 0.0):
    write_to_file(make_some_noise(bytes,noise_level), file_name)

def write_string_with_noise(string, file_name = "output.txt", noise_level = 0.0):
    write_to_file(make_some_noise(string, noise_level, is_string=True), file_name)


def count_difference_bytes(original, received):
    assert (len(original) == len(received)), "Different length of original and received"
    count = 0
    for i in range(len(original)):
        b1 = original[i]
        b2 = received[i]
        for bit in range(8):
            if (b1 & 1) != (b2 & 1):
                count+=1
            b1 >>= 1
            b2 >>= 1
    return count

def count_difference_files(file1, file2):
    bytes1 = get_bytes(file1, is_file=True)
    bytes2 = get_bytes(file2, is_file=True)
    return count_difference_bytes(bytes1, bytes2)


# dif = count_difference_files("input.txt", "input2.txt")


# dif = 24
# while dif>=20:
#     b = b"abc"
#     dif = count_difference_bytes(b, make_some_noise(b, 0.99))
#
# print(str(dif))


##work with string
# inp = "abc"
# print("input is >> ", inp)
# write_string_with_noise(inp, noise_level=0.1)


# #work with bytes
# i = b"abc"
# print("input is >> ", i)
# write_bytes_with_noise(i, noise_level=1.0)