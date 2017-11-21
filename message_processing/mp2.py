from message_processing.message_processor import process_message

import threading


def f1():
    print('1')
    for i in range(1, 6):
        file_name = 'datasets/BMP/Big/f' + str(i) + '.bmp'
        process_message(None, file_path=file_name, noise_rate=0.00)


def f2():
    print('2')

    for i in range(1, 6):
        file_name = 'datasets/WAV/Big/f' + str(i) + '.wav'
        process_message(None, file_path=file_name, noise_rate=0.00)


def f3():
    print('3')
    for i in range(1, 6):
        file_name = 'datasets/GIF/Big/f' + str(i) + '.gif'
        process_message(None, file_path=file_name, noise_rate=0.00)


def f4():
    print('4')

    for i in range(1, 6):
        file_name = 'datasets/RTF/Big/f' + str(i) + '.rtf'
        process_message(None, file_path=file_name, noise_rate=0.00)


def f5():
    print('5')
    for i in range(1, 6):
        file_name = 'datasets/TIF/Big/f' + str(i) + '.tif'
        process_message(None, file_path=file_name, noise_rate=0.00)

#
# # init threads
# t1 = threading.Thread(target=f1)
# t2 = threading.Thread(target=f2)
t3 = threading.Thread(target=f3)
t4 = threading.Thread(target=f4)
# t5 = threading.Thread(target=f5)

# # start threads
# t1.start()
# t2.start()
t3.start()
t4.start()
# t5.start()
