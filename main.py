import golay_code

# LZ78 usage:

#file_name = 'gif1.gif'     #1-3
#file_name = 'tif1.tif'     #1-10
#file_name = 'bmp5.bmp'     #1-6
#file_name = 'wav3.wav'     #1-3
#file_name = 'rtf1.rtf'     #1-3
#file_name = 'aiff1.aiff'   #1-3
file_name = 'txt1.txt'     #1-6

f = open(file_name, 'r')
input = f.read()
encoded = golay_code.encode(golay_code.tobits(input), input.__len__())
print(encoded)