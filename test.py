# import time
#
# import message_processing.iochannel as io
#
# import message_processing.compression.shannon_fano as fano
# import message_processing.encoding.repetition as rep
#
# inp = "../input.txt"
# # out = "output.txt"
# # noise = "noise.txt"
#
# begin = time.time()
#
# # read file
# print("Input file >>")
# ib = io.get_bytes(inp, is_file=True)
# # print(ib)
# print(len(ib))
# it = time.time()
# print(str(it - begin))
#
# # compress
# print("Compressed bytes >>")
# compressed = fano.compress(ib)
# # print(compressed)
# print(len(compressed))
# ct = time.time()
# print(str(ct - it))
#
# # decompress
# print("Decompressed bytes >>")
# decompressed = fano.decompress(compressed)
# # print(decompressed)
# print(len(decompressed))
# dt = time.time()
# print(str(dt - ct))
#
# m = 3
#
# # code
# print("Coded string >>")
# cb = rep.code(ib, mult=m)
# # print(cb)
# print(len(cb))
# codt = time.time()
# print(str(codt - dt))
#
# # make noize
# print("Noized string >>")
# nb = io.make_some_noise(cb, is_string=False, noise_level=0.0)
# # print(nb)
# print(len(nb))
# nt = time.time()
# print(str(nt - codt))
#
# # decode
# print("Decoded string >>")
# db = rep.encode(nb, mult=m)
# # print(db)
# print(len(db))
# dect = time.time()
# print(str(dect - nt))
#
# io.write_file(db, "kek.wav")
# # #Difference
# print("Different bits >>")
# dif = io.count_difference_bytes(ib, db)
# print(str(dif))
#
# dift = time.time()
# print(str(dift - dect))