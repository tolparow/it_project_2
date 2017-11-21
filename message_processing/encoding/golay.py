import numpy

# Number of bytes in the original file
number_of_bytes = 0

positions_of_broken_bits = []


def encode(byte_string, encoding_parameters=None):
    """ Encodes sequence of bits to encoding with special encoding parameters """
    bits = to_bits(byte_string)

    global number_of_bytes
    number_of_bytes = len(byte_string)

    final_encoding = ''

    if encoding_parameters is None:
        encoding_parameters = DEFAULT_GOLAY_CONSTANTS

    for i in range(0, number_of_bytes * 12, 12):
        temp_list = [bits[i], bits[i + 1], bits[i + 2], bits[i + 3], bits[i + 4], bits[i + 5], bits[i + 6], bits[i + 7],
                     bits[i + 8], bits[i + 9], bits[i + 10], bits[i + 11]]
        temp = numpy.array(temp_list)
        temp_list.clear()

        new_bits = numpy.array(temp).reshape((12, 1))

        res = numpy.dot(DEFAULT_G.T, new_bits)
        codeword = divmod(res.ravel(), 2)[1]
        final_encoding += _bits_to_encoding(codeword, encoding_parameters)

    return encoding_to_bytes(_from_encoding_to_bits(final_encoding))


def encoding_to_bytes(encoding):
    """
    String of bits to bytes ('0001' -> b'\x01')
    :param encoding: bitstring
    :return: bytes
    """
    return int(encoding, 2).to_bytes(len(encoding) // 8, byteorder='big')


def bytes_to_bitstring(b):
    """
    Bytes to bitstring (b'\x01' -> '0001')
    :param b: bytes
    :return: bitstring
    """
    s = ''.join(format(x, '08b') for x in b)
    return s


def decode(byte_string, encoding_parameters=None):
    """
    Decodes string of bits using 'decode_12' function to decode
    12bit-length words to encoding with special encoding parameters
    """
    if encoding_parameters is None:
        encoding_parameters = DEFAULT_GOLAY_CONSTANTS

    received_bits = _from_bits_to_encoding(bytes_to_bitstring(byte_string))

    final_encoding_sequence = ''

    number_of_all_errors = 0

    for i in range(0, number_of_bytes * 12, 12):
        temp = received_bits[i] + received_bits[i + 1] + received_bits[i + 2] + received_bits[i + 3] + \
               received_bits[i + 4] + received_bits[i + 5] + received_bits[i + 6] + received_bits[i + 7] + \
               received_bits[i + 8] + received_bits[i + 9] + received_bits[i + 10] + received_bits[i + 11]
        corrected_bits, number_errors_12 = decode_12(temp, encoding_parameters)
        global positions_of_broken_bits
        # Checking for an error
        if corrected_bits is not None:
            final_encoding_sequence += corrected_bits
        else:
            positions_of_broken_bits.append(i / 12)
            final_encoding_sequence += '____________'
        number_of_all_errors += number_errors_12

    return final_encoding_sequence, number_of_all_errors


def decode_12(string_bits_12, encoding_parameters):
    """
    Decodes string of 12 bits, using bitwise error checking
    output:
    corrected_bits in string, number_errors_12
    corrected_bits is None if 4 bit error detected
    """
    received_bits = _encoding_to_bits(string_bits_12, encoding_parameters)
    corrected_bits, number_errors_12 = decode_bits(received_bits)  # errors in # bits
    if corrected_bits is None:
        return None, number_errors_12
    else:
        return _bits_to_encoding(corrected_bits, encoding_parameters), number_errors_12


# alt name for the decode function for consistency with hamming decoding
decode_golay_12 = decode

initial_bits = b''


def get_origin():
    """ Returns original byte string with errors appeared """
    global initial_bits
    global positions_of_broken_bits
    for position in positions_of_broken_bits:
        initial_bits = initial_bits[:int(position)] + b'_' + initial_bits[int(position + 1):]
    return initial_bits


def decode_bits(received_bit_vector):
    """ Decode a received 24 bit vector to a corrected 24 bit vector with golay defaults """
    corrected_vector = numpy.dot(DEFAULT_H, received_bit_vector) % 2
    try:
        errors = numpy.array(DEFAULT_SYNDROME_LUT[tuple(corrected_vector)])
    except KeyError:
        return None, 4
    corrected = (received_bit_vector + errors) % 2  # best guess for transmitted bitvector
    return corrected, numpy.sum(errors)


def _make_3bit_errors(vector_length=24):
    """
    Return list of all bitvectors with <= 3 bits as 1's, rest 0's
    returns list of lists, each 24 bits long by default.
    """
    errorvecs = [[0] * vector_length]  # all zeros
    # one 1
    for i in range(vector_length):
        vec = [0] * vector_length
        vec[i] = 1
        errorvecs.append(vec)

    # two 1s
    for i in range(vector_length):
        for j in range(i + 1, vector_length):
            vec = [0] * vector_length
            vec[i] = 1
            vec[j] = 1
            errorvecs.append(vec)

    # three 1s
    for i in range(vector_length):
        for j in range(i + 1, vector_length):
            for k in range(j + 1, vector_length):
                vec = [0] * vector_length
                vec[i] = 1
                vec[j] = 1
                vec[k] = 1
                errorvecs.append(vec)
    return errorvecs


def _from_encoding_to_bits(encoding, encoding_parameters=None):
    """ Convert encoding string to string of bits with special encoding parameters """
    if encoding_parameters is None:
        encoding_parameters = DEFAULT_GOLAY_CONSTANTS
    bitstring = ''
    for byte in encoding:
        bitstring += encoding_parameters[byte]
    return bitstring


def _from_bits_to_encoding(bits, encoding_parameters=None):
    """ Convert string of bits to encoding of string with special encoding parameters """
    if encoding_parameters is None:
        encoding_parameters = DEFAULT_GOLAY_CONSTANTS
    bits_to_encoding = dict(zip(encoding_parameters.values(), encoding_parameters.keys()))
    encoding = ''
    for i in range(0, len(bits), 2):
        bit1 = str(int(bits[i]))
        bit2 = str(int(bits[i + 1]))
        encoding += bits_to_encoding[bit1 + bit2]
    return encoding


def to_bits(s):
    """ Convert bytes to string of bits """
    global initial_bits
    initial_bits = s
    return [int(item) for sublist in (format(x, '012b') for x in s) for item in sublist]


def from_bits(bits):
    """ Convert string of bits to bytes """
    chars = []
    for b in range(int(len(bits) / 12)):
        byte = bits[b * 12:(b + 1) * 12]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def _encoding_to_bits(encoding, encoding_parameters):
    """ Convert encoding string to string of bits with encoding parameters """
    bitstring = ''
    for entry in encoding:
        bitstring += encoding_parameters[entry]
    bits = numpy.array(list(map(int, bitstring)))
    return bits


def _bits_to_encoding(bits, encoding_parameters):
    """ Convert string of bits to encoding of string with encoding parameters """
    bits_to_encoding = dict(zip(encoding_parameters.values(), encoding_parameters.keys()))
    encoding = ''
    for i in range(0, len(bits), 2):  # take bits in twos
        bit1 = str(int(round(bits[i])))
        bit2 = str(int(round(bits[i + 1])))
        encoding += bits_to_encoding[bit1 + bit2]
    return encoding


# end support fns


# Constants
DEFAULT_GOLAY_CONSTANTS = {"A": "11", "O": "00", "U": "10", "G": "01"}

# Parity submatrix P
DEFAULT_P = numpy.array([
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, ],
    [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, ],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, ],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, ],
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, ],
    [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, ],
    [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, ],
    [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, ],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, ],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, ],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, ],
], dtype='int')

# Generator mtx G, where transmitted codewords (24bits) are
# G.T dot msg or (msg dot G) (msg is 12 bit message)
# 2**12 = 4096 total codewords, one for each msg
# (all mod 2 arithmetic)
# other G matrices give golay (24,12,8) codes, but this one
# matches existing codes from pre 2010 used in knight lab
DEFAULT_G = numpy.concatenate((DEFAULT_P, numpy.eye(12, dtype="int")), axis=1)

# Parity check matrix H satisfies G dot H.T = zeros (mod 2 arithmetic)
# also satisfies syn = H dot rec = H dot err (rec is recieved 24 bits,
# err is 24 bit error string added to transmitted 24 bit vec)
# (all mod 2 arithmetic)
DEFAULT_H = numpy.concatenate((numpy.eye(12, dtype="int"), DEFAULT_P.T), axis=1)

_ALL_3BIT_ERRORS = _make_3bit_errors()

# Lookup table
DEFAULT_SYNDROME_LUT = {}

# Build lookup table
for error_vector in _ALL_3BIT_ERRORS:
    syn = tuple(numpy.dot(DEFAULT_H, error_vector) % 2)
    DEFAULT_SYNDROME_LUT[syn] = error_vector
