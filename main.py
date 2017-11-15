import sys
import time
import golay_code

# Golay usage:

# file_name = 'gif1.gif'     #1-3
# file_name = 'tif4.tif'     #1-10
# file_name = 'bmp1.bmp'     #1-6
# file_name = 'wav3.wav'     #1-3
# file_name = 'rtf1.rtf'     #1-3
# file_name = 'aiff1.aiff'   #1-3
file_name = 'txt1.txt'     #1-6

f = open(file_name, 'rb')
input = f.read()
print('Size in bytes before encoding : ' + str(sys.getsizeof(input)))
current_milli_time_before = int(round(time.time() * 1000))
encoded = golay_code.encode(golay_code.to_bits(input), len(input))
current_milli_time_after = int(round(time.time() * 1000))
print('Size in bytes after encoding : ' + str(sys.getsizeof(encoded)))
print('Time taken by encoding : ' + (current_milli_time_after - current_milli_time_before).__str__() + ' ms')
current_milli_time_before = int(round(time.time() * 1000))
decoded = golay_code.decode(encoded)
current_milli_time_after = int(round(time.time() * 1000))
print('Time taken by decoding  : ' + (current_milli_time_after - current_milli_time_before).__str__() + ' ms')
print('Number of errors were detected - ', decoded[1])
file_name = file_name.split('.')[0] + 'AfterEncoding' + file_name.split('.')[1]
f = open(file_name, 'wb')
f.write(golay_code.get_origin())
f.close()