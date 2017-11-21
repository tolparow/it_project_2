import rlp
import time


def get_bytes(obj, is_file=False):
    if is_file:
        with open(obj, 'rb') as f:
            return f.read()

    assert isinstance(obj, str), 'The object is neither string nor file path!'
    return bytes(obj, 'utf-8')


def get_str(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


def compress(uncompressed):
    """Compress a string of bytes to a list of bytes and integer positions"""

    # Build the dictionary
    dictionary_size = 256
    
    dictionary = dict((bytes([i]), bytes([i])) for i in range(dictionary_size))

    # Applying compression algorithm
    single_byte = b''
    compressed = []
    for byte in uncompressed:
        temp_bytes = single_byte + bytes([byte])
        if temp_bytes in dictionary:
            single_byte = temp_bytes
        else:
            compressed.append(dictionary[single_byte])
            dictionary[temp_bytes] = dictionary_size
            dictionary_size += 1
            single_byte = bytes([byte])

    if single_byte:
        compressed.append(dictionary[single_byte])
        
    return rlp.encode(compressed)


def decompress(compressed):
    """Decompress a list of bytes to original string of bytes"""

    compressed = rlp.decode(compressed)
    
    # Build the dictionary of integers, as.
    dictionary_size = 256
    dictionary = dict((i, i) for i in range(dictionary_size))

    # Applying decompression algorithm
    decompressed = []
    single_byte = compressed.pop(0)
    decompressed.append(single_byte)
    for list_entry in compressed:
        if isinstance(list_entry, bytes):
            list_entry = int.from_bytes(list_entry, 'big')
        if list_entry in dictionary:
            entry = bytes([dictionary[list_entry]]) if isinstance(dictionary[list_entry], int) else dictionary[list_entry]
        elif list_entry == dictionary_size:
            entry = single_byte + bytes([single_byte[0]])
        else:
            raise ValueError('Cannot decompress list entry: %s' % list_entry)
        decompressed.append(entry)

        # Add combinations of entries to the dictionary.
        dictionary[dictionary_size] = single_byte + bytes([entry[0]])
        dictionary_size += 1

        single_byte = entry

    return b''.join(decompressed)
