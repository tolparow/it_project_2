from bitarray import bitarray

def __separator():
    return 0x01011.to_bytes(2, "big")

def compress(message: bytes):
    """
    Shannon-Fano compress

    :return: compressed file with alphabet
    """
    bytes = bytearray(message)
    # count symbols
    freq = [0] * 256
    for b in bytes:
        freq[b] += 1

    # add lists [val, freq, code] with nonzero frequency to tuplist
    tuplist = []
    for i in range(256):
        if freq[i] > 0:
            # XXX: ошибка с неправильным обратным отображением может быть тут. исмволы типа: "\x80"
            tuplist.append([i, freq[i], ''])

    #sort tuplist by frequency
    stuplist = sorted(tuplist, key=lambda tup: tup[1], reverse=True)
    # stuplist.append((len(tuplist), 0, '')) #Separator
    alph = __requr_work(stuplist, 0, len(stuplist) - 1)
    # len of alphabet
    part1 = str(len(alph)) + __separator().decode()
    # bytes with alphabet in format: 'letter''code''separator'...
    part2 = b''
    for i in alph:
        # TODO: short cycle
        part2 += (i[0]).to_bytes(1, byteorder='big')
        part2 += (__prepare_bytes(i[2]))
        part2 += __separator()

    alphabet = {}
    for i in alph:
        alphabet[i[0]] = i[2]
    print(alphabet)
    # message
    part3 = ''
    for b in bytes:
        part3 += alphabet[b]

    result = part1.encode() + part2 + __prepare_bytes(part3)
    return result



def decompress(message: bytes):
    """
    Shannon-Fano decompress
    Send bytes ONLY!!

    :return: decompressed message bytes
    """
    # 1. Restore alphabet
    num = int(message.split(__separator())[0])
    alph = message.split(__separator())[1:num + 1]
    alphabet = {}
    for i in alph:
        alphabet[__restore_bits(i[1:])] = i[0].to_bytes(1, 'big') #string->bytes

    # 2. Restore message
    tmp = message.split(__separator())[num + 1:][0]
    msg = __restore_bits(tmp)
    restored = b''
    tmp = ''
    for bit in msg:
        tmp += str(int(bit))
        if tmp in alphabet:
            restored += alphabet[tmp]
            tmp = ''

    return restored


def __prepare_bytes(bins):
    """
    monitors bits to fully 8bit first byte and other sequence is same bytes without changes

    :param bins: string with '0' and '1'
    :return: bytes
    """
    # first bit is to monitor valuable zeros
    bins = '1' + bins
    bins = '0' * int(8 - len(bins) % 8) + bins
    return bitarray(bins).tobytes()

def __requr_work(stuplist, begin, end):
    """
    recurrently creates alphabet

    :param stuplist: splited tuple list
    :param begin: index of current step begin
    :param end: index of current step end
    :return: alphabet with codes
    """
    if begin >= end:
        return stuplist
    itop = begin
    ibot = end

    top = stuplist[begin][1]
    bot = 0
    # find middle
    for i in range(begin, end - 1):
        if top <= bot:
            top += stuplist[itop][1]
            itop += 1
            if ibot == itop:
                itop -= 1
                break
        else:
            bot += stuplist[ibot][1]
            ibot -= 1
            if ibot == itop:
                ibot += 1
                break
    # update codes
    for i in range(begin, end + 1):
        if i <= itop:
            stuplist[i][2] += '0'
        else:
            stuplist[i][2] += '1'
    stuplist = __requr_work(stuplist, begin, itop)
    stuplist = __requr_work(stuplist, ibot, end)
    return stuplist



def __restore_bits(bytes: bytes):
    """
    correctly parses compressed bytes to bitarray, due to 00...001 prefix in unfully bytes

    :param bytes: received from channel bytes
    :return: correct bitarray
    """
    bits = bitarray()
    bits.frombytes(bytes)
    while not bits.pop(0):
        continue
    return bits.to01() #string
