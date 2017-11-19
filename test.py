import coding.repetition as rep
import compressing.shannon_fano as fano
import noize.iochannel as io

inp = "../input.txt"
# out = "output.txt"
# noise = "noise.txt"

#read file
print("Input file >>")
ib = io.get_bytes(inp, is_file=True)
print(ib)

#compress
print("Compressed bytes >>")
compressed = fano.compress(ib)
print(compressed)

#decompress
print("Decompressed bytes >>")
decompressed = fano.decompress(compressed)
print(decompressed)

m = 3

#code
print("Coded string >>")
cb = rep.code(ib, mult=m)
print(cb)

#make noize
print("Noized string >>")
nb = io.make_some_noise(cb, is_string=False, noise_level=0.01)
print(nb)

#decode
print("Decoded string >>")
db = rep.encode(nb, mult=m)
print(db)

#Difference
print("Different bits >>")
dif = io.count_difference_bytes(ib, db)
print(str(dif))