import numpy

number_of_symbols = 0

initial_bits = ''


def _from_encoding_to_bits(s, nt_to_bits=None):
    if nt_to_bits is None:
        nt_to_bits = DEFAULT_GOLAY_NT_TO_BITS
    bitstring = ''
    for nt in s:
        bitstring += nt_to_bits[nt]
    return bitstring


def _from_bits_to_encoding(bits, nt_to_bits=None):
    if nt_to_bits is None:
        nt_to_bits = DEFAULT_GOLAY_NT_TO_BITS
    bits_to_nt = dict(zip(nt_to_bits.values(), nt_to_bits.keys()))
    seq = ""
    for i in range(0, len(bits), 2):  # take bits in twos
        bit1 = str(int(bits[i]))
        bit2 = str(int(bits[i + 1]))
        seq += bits_to_nt[bit1 + bit2]
    return seq


def to_bits(s):
    global initial_bits
    initial_bits = s
    return [int(item) for sublist in (format(x, '012b') for x in s) for item in sublist]


def from_bits(bits):
    chars = []
    for b in range(int(len(bits) / 12)):
        byte = bits[b * 12:(b + 1) * 12]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def decode(seq, nt_to_bits=None):
    if nt_to_bits is None:
        nt_to_bits = DEFAULT_GOLAY_NT_TO_BITS

    received_bits = seq

    final_seq = ''

    number_of_errors = 0

    for i in range(0, number_of_symbols * 12, 12):
        temp = received_bits[i] + received_bits[i + 1] + received_bits[i + 2] + received_bits[i + 3] + \
               received_bits[i + 4] + received_bits[i + 5] + received_bits[i + 6] + received_bits[i + 7] + \
               received_bits[i + 8] + received_bits[i + 9] + received_bits[i + 10] + received_bits[i + 11]
        # print(temp)
        corrected_bits, num_errors = decode_12(temp, nt_to_bits)
        if corrected_bits != None:
            final_seq += corrected_bits
        else:
            final_seq += '____________'
        number_of_errors += num_errors

    return final_seq, number_of_errors


def decode_12(seq, nt_to_bits):
    """decodes a nucleotide string of 12 bases, using bitwise error checking
    inputs:
    - seq, a string of nucleotides
    - nt_to_bits, e.g.: { "A":"11",  "C":"00", "T":"10", "G":"01"}
    output:
    corrected_seq (str), num_bit_errors
    corrected_seq is None if 4 bit error detected"""
    received_bits = _seq_to_bits(seq, nt_to_bits)
    corrected_bits, num_errors = decode_bits(received_bits)  # errors in # bits
    if corrected_bits is None:
        return None, num_errors
    else:
        # put match into nucleotide format
        return _bits_to_seq(corrected_bits, nt_to_bits), num_errors


# alt name for the decode function for consistency with hamming decoding
decode_golay_12 = decode


def encode(bits, n, nt_to_bits=None):
    """ takes any 12 bits, returns the golay 24bit codeword in nucleotide format
    bits is a list/array, 12 long, e.g.: [0,0,0,0,0,0,0,0,0,1,0,0]
    nt_to_bits is e.g.: {"A":"11", "C":"00", "T":"10", "G":"01"}, None => default
    output is e.g.: 'AGTCTATTGGCT'
    """
    global number_of_symbols
    number_of_symbols = n

    final_seq = ''

    if nt_to_bits is None:
        nt_to_bits = DEFAULT_GOLAY_NT_TO_BITS

    for i in range(0, number_of_symbols * 12, 12):
        temp_list = []
        temp_list.append(bits[i])
        temp_list.append(bits[i + 1])
        temp_list.append(bits[i + 2])
        temp_list.append(bits[i + 3])
        temp_list.append(bits[i + 4])
        temp_list.append(bits[i + 5])
        temp_list.append(bits[i + 6])
        temp_list.append(bits[i + 7])
        temp_list.append(bits[i + 8])
        temp_list.append(bits[i + 9])
        temp_list.append(bits[i + 10])
        temp_list.append(bits[i + 11])
        temp = numpy.array(temp_list)
        temp_list.clear()

        new_bits = numpy.array(temp).reshape((12, 1))

        # cheap way to do binary xor in matrix dot
        res = numpy.dot(DEFAULT_G.T, new_bits)
        codeword = divmod(res.ravel(), 2)[1]
        final_seq += _bits_to_seq(codeword, nt_to_bits)

    return final_seq


def get_origin(n_errors):
    if n_errors >= 4:
        return None
    else:
        return initial_bits


def decode_bits(received_bitvec):
    """ decode a received 24 bit vector to a corrected 24 bit vector
    uses golay defaults
    input: received bitvec is 24 bits long, listlike
    output: corrected_vec, num_bit_errors
    corrected_vec is None iff num_errors = 4"""
    rec = received_bitvec
    syn = numpy.dot(DEFAULT_H, rec) % 2
    try:
        err = numpy.array(DEFAULT_SYNDROME_LUT[tuple(syn)])
    except KeyError:
        return None, 4
    corrected = (rec + err) % 2  # best guess for transmitted bitvector
    return corrected, numpy.sum(err)


# begin support fns


def _make_3bit_errors(veclen=24):
    """ return list of all bitvectors with <= 3 bits as 1's, rest 0's
    returns list of lists, each 24 bits long by default.
    not included:
    [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0]
    included:
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    """
    errorvecs = []
    # all zeros
    errorvecs.append([0] * veclen)
    # one 1
    for i in range(veclen):
        vec = [0] * veclen
        vec[i] = 1
        errorvecs.append(vec)

    # two 1s
    for i in range(veclen):
        for j in range(i + 1, veclen):
            vec = [0] * veclen
            vec[i] = 1
            vec[j] = 1
            errorvecs.append(vec)

    # three 1s
    for i in range(veclen):
        for j in range(i + 1, veclen):
            for k in range(j + 1, veclen):
                vec = [0] * veclen
                vec[i] = 1
                vec[j] = 1
                vec[k] = 1
                errorvecs.append(vec)
    return errorvecs


def _seq_to_bits(seq, nt_to_bits):
    """ e.g.: "AAG" -> array([0,0,0,0,1,0])
    output is array of ints, 1's and 0's
    nt_to_bits is e.g.: {"A":"11", "C":"00", "T":"10", "G":"01"}
    """
    bitstring = ''
    for nt in seq:
        bitstring += nt_to_bits[nt]
    bits = numpy.array(list(map(int, bitstring)))
    # print('bits')
    # print(bits)
    return bits


def _bits_to_seq(bits, nt_to_bits):
    """ e.g.: array([0,0,0,0,1,0]) -> "AAG"
    nt_to_bits is e.g.: {"A":"11", "C":"00", "T":"10", "G":"01"}
    """
    # print(bits)
    bits_to_nt = dict(zip(nt_to_bits.values(), nt_to_bits.keys()))
    seq = ""
    for i in range(0, len(bits), 2):  # take bits in twos
        bit1 = str(int(round(bits[i])))
        bit2 = str(int(round(bits[i + 1])))
        seq += bits_to_nt[bit1 + bit2]
    return seq


# end support fns


# BEGIN module level constants
DEFAULT_GOLAY_NT_TO_BITS = {"A": "11", "O": "00", "U": "10", "G": "01"}

# We use this matrix as the parity submatrix P
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
], dtype='int')  # from http://courses.csusm.edu/math540ak/codes.pdf

# generator mtx G, where transmitted codewords (24bits) are
# G.T dot msg or (msg dot G) (msg is 12 bit message)
# 2**12 = 4096 total codewords, one for each msg
# (all mod 2 arithmetic)
# other G matrices give golay (24,12,8) codes, but this one
# matches existing codes from pre 2010 used in knight lab
DEFAULT_G = numpy.concatenate((DEFAULT_P, numpy.eye(12, dtype="int")), axis=1)

# pairity check matrix H satisfies G dot H.T = zeros (mod 2 arithmetic)
# also satisfies syn = H dot rec = H dot err (rec is recieved 24 bits,
# err is 24 bit error string added to transmitted 24 bit vec)
# (all mod 2 arithmetic)
DEFAULT_H = numpy.concatenate((numpy.eye(12, dtype="int"), DEFAULT_P.T), axis=1)

_ALL_3BIT_ERRORS = _make_3bit_errors()
# len = 2325.  (1 (all zeros) + 24 (one 1) + 276 (two 1s) + 2024)

# syndrome lookup table is the key to (fast, syndrome) decoding
# decode() uses syndrome lookup table

DEFAULT_SYNDROME_LUT = {}
# key: syndrome (12 bits).  Val: 24 bit err for that syn
# we include the all zeros error (key = all zeros syndrome)


# build syndrome lookup table
for errvec in _ALL_3BIT_ERRORS:
    syn = tuple(numpy.dot(DEFAULT_H, errvec) % 2)
    DEFAULT_SYNDROME_LUT[syn] = (errvec)
