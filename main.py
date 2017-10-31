import lz
import sys
import time

# LZ78 and usage:
print('Size in bytes before compressing : ' + sys.getsizeof(lz.get_str('sample.txt')).__str__())
current_milli_time_before = int(round(time.time() * 1000))
compressed = lz.compress(lz.get_str('sample.txt'))
current_milli_time_after = int(round(time.time() * 1000))
print('Size in bytes after compressing : ' + lz.size_of_compressed.__str__())
print('Time taken by compressing : ' + (current_milli_time_after - current_milli_time_before).__str__() + ' ms')
decompressed = lz.decompress(compressed)