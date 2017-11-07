from noize import iochannel as io

def compress(message, is_string=True):
    bytes = bytearray()
    if is_string:
        bytes = bytearray(message, 'utf8')
    else:
        bytes = message[:]
    # count symbols
    freq = [0] * 256
    for b in bytes:
        freq[b] += 1
    print(freq)

    # add lists [val, freq, code] with nonzero frequency to tuplist
    tuplist = []
    for i in range(256):
        if freq[i] > 0:
            #XXX: ошибка с неправильным обратным отображением может быть тут. исмволы типа: "\x80"
            tuplist.append([chr(i), freq[i], ''])

    # sort tuplist by frequency
    stuplist = sorted(tuplist, key=lambda tup: tup[1], reverse=True)
    print(stuplist)

    alphabet = requr_work(stuplist, 0 , len(stuplist))

# def requr_work(stuplist, begin, end):
#     if (end-begin) <= 1:
#

compress(io.get_bytes("../input.txt", is_file=True), is_string=False)