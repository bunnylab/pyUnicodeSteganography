CHAR_OFFSET = 32 # skip control chars
START_EMOJI = ord('\U0001F601') 

def encode(msg, binary=False):
    '''
    Encode a message using emojis
    '''
    new_str = ''
    
    if binary:
        msg_bytes = msg
    else:
        msg_bytes = bytes(msg, 'utf-8')
    
    for b in msg_bytes:
        #print(b + START_EMOJI - CHAR_OFFSET)
        new_str = new_str + chr(b + START_EMOJI - CHAR_OFFSET)


    return new_str


def decode(msg, binary=False):
    '''
    Decode a message using emojis
    '''
    new_str = '' 
    new_bytes = b''

    for c in msg:
        if binary:
           new_bytes = new_bytes + (ord(c) - START_EMOJI + CHAR_OFFSET).to_bytes(1, byteorder='big')
        else:
            new_str = new_str + chr(ord(c) - START_EMOJI + CHAR_OFFSET)

    if binary:
        return new_bytes
    return new_str