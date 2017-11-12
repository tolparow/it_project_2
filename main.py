import lz
import sys
import time
import rlp

# LZ78 usage:

#file_name = 'gif1.gif'     #1-3
#file_name = 'tif1.tif'     #1-10
#file_name = 'bmp5.bmp'     #1-6
#file_name = 'wav3.wav'     #1-3
#file_name = 'rtf1.rtf'     #1-3
#file_name = 'aiff1.aiff'   #1-3
#file_name = 'txt1.txt'     #1-6
print('Size in bytes before compressing : ' + sys.getsizeof(lz.get_str(file_name)).__str__())
current_milli_time_before = int(round(time.time() * 1000))
compressed = lz.compress(lz.get_bytes(file_name, True))
current_milli_time_after = int(round(time.time() * 1000))
print('Size in bytes after compressing : ' + sys.getsizeof(rlp.encode(compressed)).__str__())
print('Time taken by compressing : ' + (current_milli_time_after - current_milli_time_before).__str__() + ' ms')
decompressed = (lz.decompress(compressed)).encode()
f = open('test', 'wb')
f.write(decompressed)
f.close()