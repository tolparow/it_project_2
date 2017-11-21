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


def make_some_noise(message, noise_level=0.0, is_string=False):
    """
    add noise to message

    :param message: input data
    :param noise_level: real number in range [0..1]
    :param is_string: is it string or bytes
    :return: noised bytes
    """
    assert (noise_level >= 0 and noise_level <= 1), (
    "Wrong value of noise_level! " + str(noise_level) + " not in [0;1]  ")
    set_of_bytes = bytearray()
    if is_string:
        set_of_bytes = bytearray(message, 'utf-8')
    else:
        set_of_bytes = bytearray(message)

    for index, byte in enumerate(set_of_bytes):  # for every byte
        tmp = 0
        b = byte
        for i in range(8):  # for every bit
            tmp >>= 1
            if random.random() < noise_level:
                # reverse
                tmp += 128 * (1 - b & 1)
            else:
                # save like in input
                tmp += 128 * (b & 1)
            b >>= 1
        set_of_bytes[index] = tmp
    return set_of_bytes


def write_file(content, file_name="output.txt", is_string=False):
    if is_string:
        with open(file_name, 'w') as f:
            f.write(content)
    else:
        with open(file_name, 'wb') as f:
            f.write(content)


def write_bytes_with_noise(bytes, file_name="output.txt", noise_level=0.0):
    """
    Write bytes and swipes some their bits with probability of swap @noise_level
    to file with name @file_name

    :param bytes: input sequence
    :param file_name: path to output file
    :param noise_level: real number in range [0..1]
    """
    write_file(make_some_noise(bytes, noise_level), file_name)


# Write string and swipes some their bits with probability of swap @noise_level
# to file with name @file_name
def write_string_with_noise(string, file_name="output.txt", noise_level=0.0):
    write_file(make_some_noise(string, noise_level, is_string=True), file_name)


def count_difference_bytes(original: bytes, received: bytes):
    """
    Find number of bits which are different in two objects of type bytes()

    :param original: bytes from original file
    :param received: bytes after noise decoded
    :return: number of bits that are not equal in original and received
    """
    assert (len(original) == len(received)), "Different length of original and received"
    count = 0
    for i in range(len(original)):
        b1 = original[i]
        b2 = received[i]
        for bit in range(8):
            if (b1 & 1) != (b2 & 1):
                count += 1
            b1 >>= 1
            b2 >>= 1
    return count


def count_difference_files(file1: str, file2: str):
    """
    Find number of bits which are different in two files with paths @file1, @file2

    :param file1: path to file
    :param file2: path to file
    :return: number of bits that are not equal in original and received
    """
    bytes1 = get_bytes(file1, is_file=True)
    bytes2 = get_bytes(file2, is_file=True)
    return count_difference_bytes(bytes1, bytes2)
