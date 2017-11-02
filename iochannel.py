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

def make_some_noize(bytes, noize_level = 0.0, is_string=False):
    print ("\nin function >> ")
    assert(noize_level >= 0 and noize_level <= 1), ("Wrong value of noize_level! " + str(noize_level) + " not in [0;1]  ")


    set_of_bytes = bytearray()

    if is_string:
        set_of_bytes = bytearray(bytes, 'utf-8')
    else:
        set_of_bytes = bytearray(bytes)

    for index, byte in enumerate(set_of_bytes):  #for every byte
        tmp = 0
        print(byte)
        b = byte
        for i in range(8): #for every bit
            tmp >>= 1
            if random.random() < noize_level:
                print("Randomed")
                #reverse
                tmp += 128 * (1 - b & 1)
            else:
                #save like in input
                tmp += 128 * (b & 1)
            b >>= 1
        set_of_bytes[index] = tmp
    return set_of_bytes

def write_to_file(content, file_name = "output.txt", is_string = False):
    print(content)

    if is_string:
        with open(file_name, 'w') as f:
            f.write(content)
    else:
        with open(file_name, 'wb') as f:
            f.write(content)


def write_bytes_with_noize(bytes, file_name = "output.txt", noize_level = 0.0):
    write_to_file(make_some_noize(bytes,noize_level), file_name)

def write_string_with_noize(string, file_name = "output.txt", noize_level = 0.0):
    write_to_file(make_some_noize(string, noize_level, is_string=True), file_name)

##work with string
# inp = "abc"
# print("input is >> ", inp)
# write_string_with_noize(inp, noize_level=0.1)



# #work with bytes
# i = b"abc"
# print("input is >> ", i)
# write_bytes_with_noize(i, noize_level=1.0)