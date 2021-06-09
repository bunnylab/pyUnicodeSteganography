import re
import pyUnicodeSteganography.zerowidth as zerowidth
import pyUnicodeSteganography.lookalikes as lookalikes
import pyUnicodeSteganography.snow as snow

def encode(unencoded_string, msg, method="zw", binary=False, replacements=None, delimiter=None):
    '''
    Main encoding method
    Dispatches to corresponding encoder based on specified method and handles
    insertion/appending etc. of message into the string.
    '''
    if method == "zw":
        midpoint = len(unencoded_string)//2
        if not delimiter:
            delimiter = '\u2062\u2062'
        code = delimiter + zerowidth.encode(msg, character_set=replacements, binary=binary) + delimiter

        return unencoded_string[:midpoint] + code + unencoded_string[midpoint:]

    if method == "snow":
        if not delimiter:
            delimiter = '\t\t\t'
        code = snow.encode(msg, character_set=replacements, binary=binary)
        return unencoded_string + delimiter + code

    if method == "lookalike":
        return lookalikes.encode(unencoded_string, msg, substitution_table=replacements, binary=binary)


def decode(encoded_string, method="zw", binary=False, replacements=None, delimiter=None):
    '''
    Main decoding method
    Dispatches to corresponding decoder based on specified method and handles
    extraction of encoded message from the string.
    '''
    if method == "zw":
        if not delimiter:
            delimiter = '\u2062\u2062'
        regex = "{}(.+){}".format(delimiter, delimiter)
        m = re.search(regex, encoded_string)
        code = m.groups()[0]

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


