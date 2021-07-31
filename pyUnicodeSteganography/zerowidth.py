zwc_4 = ["\u200C", "\u200D", "\u200E", "\u200F"]

def encode(msg, binary=False, character_set=None):
    '''
    Encode a message using specified set of zero width characters.
    '''
    code = ''
    if not character_set:
        character_set = zwc_4
    if binary:
        msg_bytes = msg
    else:
        msg_bytes = bytes(msg, 'utf-8')
    for by in msg_bytes:
        bit_mask = 0b00000011

        for i in range(4):
            m_byte = by & bit_mask
            by = by >> 2

            if m_byte == 3:
                code += character_set[3]
            elif m_byte == 2:
                code += character_set[2]
            elif m_byte == 1:
                code += character_set[1]
            elif m_byte == 0:
                code += character_set[0]

    return code

def decode(code, binary=False, character_set=None):
    '''
    Decode a message using specified set of zero width characters.
    '''
    msg_bytes = []
    if not character_set:
        character_set = zwc_4

    # range behave a little weird here is there a less hacky solution?
    for i in range(4, len(code)+1, 4):
        m_byte = 0b00000000
        encoded_byte = code[i-4:i]

        for j in range(4):
            m_byte = m_byte >> 2
            if encoded_byte[j] == character_set[3]:
                m_byte = m_byte | 0b11000000
            elif encoded_byte[j] == character_set[2]:
                m_byte = m_byte | 0b10000000
            elif encoded_byte[j] == character_set[1]:
                m_byte = m_byte | 0b01000000
            elif encoded_byte[j] == character_set[0]:
                pass

        msg_bytes.append(m_byte)

    if binary:
        return bytes(msg_bytes)
    return bytes(msg_bytes).decode('utf-8')
