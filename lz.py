import sys

size_of_compressed = 0

def get_bytes(obj, is_file=False):
    if is_file:
        with open(obj, 'rb') as f:
            return f.read()

    assert isinstance(obj, str), 'The object is neither string nor file path!'
    return bytes(obj, 'utf-8')


def get_str(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def update_string(byte_string):
    #print(byte_string)
    updated_string = ''
    temp = byte_string.__str__()
    for c in temp:
        if c == '\\':
            updated_string += ' \\'
        else:
            updated_string += c
    return updated_string

def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # print(uncompressed)
    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in range(dict_size))
    # in Python 3: dictionary = {chr(i): chr(i) for i in range(dict_size)}

    w = ''
    result = []
    for c in uncompressed:
        wc = w + chr(c)
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = chr(c)

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    # print(result)
    return result


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in range(dict_size))
    # in Python 3: dictionary = {chr(i): chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = compressed.pop(0)
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()
