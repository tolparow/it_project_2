from bitarray import bitarray
from noize import iochannel as io

def separator():
    return 0x0001.to_bytes(2, "big")

def compress(message, out_file="output.txt"):
    bytes = message[:]
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

    # sort tuplist by frequency
    stuplist = sorted(tuplist, key=lambda tup: tup[1], reverse=True)

    alph = requr_work(stuplist, 0, len(stuplist) - 1)


    # len of alphabet
    part1 = str(len(alph)) + separator().decode()
    # bytes with alphabet in format: 'letter''code''separator'...
    part2 = b''
    for i in alph:
        # TODO: short cycle
        part2 += (i[0]).to_bytes(1, byteorder='big')
        part2 += (prepare_bytes(i[2]))
        part2 += separator()

    # print("Alphabet:")
    # print(alph)
    alphabet = {}
    for i in alph:
        alphabet[i[0]] = i[2]
    print(alphabet)  # int[0..256] -> binString
    # message
    part3 = ''
    for b in bytes:
        part3 += alphabet[b]


    print(part3)

    result = part1.encode() + part2 + prepare_bytes(part3)#bitarray(part3).tobytes()
    # print(result)
    io.write_file(result, is_string=False, file_name="input.txt")


def prepare_bytes(bins):
    # first bit is to monitor valuable zeros
    bins = '1' + bins
    bins = '0' * int(8 - len(bins) % 8) + bins
    # if len(bins) > 8:
    #     print("PREPARED MESSAGE: ")
    #     print(bins)
    # tmp = ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(bins)] * 8))
    # return tmp[::-1].encode()
    return bitarray(bins).tobytes()

def requr_work(stuplist, begin, end):
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
    stuplist = requr_work(stuplist, begin, itop)
    stuplist = requr_work(stuplist, ibot, end)
    return stuplist

#Send bytes ONLY!!
def decompress(message: bytes, out_file="output.txt"):
    # 1. Restore alphabet
    num = int(message.split(separator())[0])

    print(num)

    alph = message.split(separator())[1:num + 1]
    alphabet = {}
    for i in alph:
        print(i)
        alphabet[restore_bits(i[1:])] = i[0].to_bytes(1, 'big') #string->bytes
    print(alphabet)

    # 2. Restore message
    tmp = message.split(separator())[num + 1:][0]
    msg = restore_bits(tmp)
    # print("MESSAGE:")
    # print(msg)

    restored = b''
    tmp = ''
    for bit in msg:
        tmp += str(int(bit))
        if tmp in alphabet:
            restored += alphabet[tmp]
            tmp = ''
    print("restored:")
    print(restored)
    io.write_file(restored, is_string=False, file_name=out_file)

def restore_bits(bytes: bytes):
    bits = bitarray()
    bits.frombytes(bytes)
    while not bits.pop(0):
        continue
    return bits.to01() #string

# compress(io.get_bytes("../input.txt", is_file=True), out_file="input.txt")
# print("<<<<<<<<<<<<DECOMPRESS>>>>>>>>>>>>")
# decompress(io.get_bytes("input.txt", is_file=True), out_file="output.txt")
# res = io.count_difference_files("../input.txt", "output.txt")
# print(str(res))