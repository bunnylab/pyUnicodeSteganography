import re
import pyUnicodeSteganography.zerowidth as zerowidth
import pyUnicodeSteganography.lookalikes as lookalikes
import pyUnicodeSteganography.snow as snow

from pyUnicodeSteganography.zerowidth import zwc_4

def encode(unencoded_string, msg, method="zw", binary=False, replacements=None, delimiter=None):
    '''
    Main encoding method
    Dispatches to corresponding encoder based on specified method and handles
    insertion/appending etc. of message into the string.
    '''
    if method == "zw":
        
        code = zerowidth.encode(msg, character_set=replacements, binary=binary)
        chars = list(unencoded_string)
        split_code = [code[i:i+4] for i in range(0, len(code), 4)]

        if len(split_code) >= len(chars):
            raise ValueError("String too short to encode message")

        out = ''
        for i in range(len(chars)):
            out = out + chars[i]
            if i < len(split_code):
                out = out + split_code[i]

        return out

    if method == "snow":
        if not delimiter:
            delimiter = '\t\t\t'
        code = snow.encode(msg, character_set=replacements, binary=binary)
        return unencoded_string + delimiter + code

    if method == "lookalike":
        return lookalikes.encode(unencoded_string, msg, substitution_table=replacements, binary=binary)

    else:
        raise Exception("Method: {}, is not supported".format(method))


def decode(encoded_string, method="zw", binary=False, replacements=None, delimiter=None):
    '''
    Main decoding method
    Dispatches to corresponding decoder based on specified method and handles
    extraction of encoded message from the string.
    '''
    if method == "zw":
        if not replacements:
            replacements = zwc_4
        code = ''
        for c in encoded_string:
            if c in replacements:
                code = code + c

        return zerowidth.decode(code, character_set=replacements, binary=binary)

    elif method == "snow":
        if not delimiter:
            delimiter = '\t\t\t'
        regex = "{}(.+)$".format(delimiter)
        m = re.search(regex, encoded_string)
        code = m.groups()[0]

        return snow.decode(code, character_set=replacements, binary=binary)

    elif method == "lookalike":
        return lookalikes.decode(encoded_string, substitution_table=replacements, binary=binary)


