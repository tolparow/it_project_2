import sys
import time
import lz
import golay_code

# Golay and LZ78 usage:

# file_name = 'gif1.gif'     #1-3
# file_name = 'tif7.tif'     #1-10
# file_name = 'bmp5.bmp'     #1-6
# file_name = 'wav1.wav'     #1-3
# file_name = 'rtf1.rtf'     #1-3
# file_name = 'aiff1.aiff'   #1-3
# file_name = 'txt4.txt'  # 1-6

print('Size in bytes before compressing : ' + sys.getsizeof(lz.get_str(file_name)).__str__())
current_milli_time_before = int(round(time.time() * 1000))
compressed = lz.compress(lz.get_bytes(file_name, True))
current_milli_time_after = int(round(time.time() * 1000))
print('Size in bytes after compressing : ' + sys.getsizeof(compressed).__str__())
print('Time taken by compressing : ' + (current_milli_time_after - current_milli_time_before).__str__() + ' ms')
current_milli_time_before = int(round(time.time() * 1000))
decompressed = lz.decompress(compressed)
current_milli_time_after = int(round(time.time() * 1000))
print('Time taken by decompressing : ' + (current_milli_time_after - current_milli_time_before).__str__() + ' ms')
output_file_name = file_name.split('.')[0] + 'AfterCompression.' + file_name.split('.')[1]
f = open(output_file_name, 'wb')
f.write(decompressed)
f.close()
