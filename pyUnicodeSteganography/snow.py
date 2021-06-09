snow_2 = [" ", "\t"]

def encode(msg, character_set=None, binary=False):
    code = ''
    if not character_set:
        character_set = snow_2
    if binary:
        msg_bytes = msg
    else:
        msg_bytes = bytes(msg, 'utf-8')
    for by in msg_bytes:
        bit_mask = 0b00000001
        for i in range(8):
            m_byte = by & bit_mask
            by = by >> 1
            if m_byte == 1:
                code += character_set[1]
            elif m_byte == 0:
                code += character_set[0]

    return code

def decode(code, character_set=None, binary=False):
    msg_bytes = []
    if not character_set:
        character_set = snow_2

    # range behave a little weird here is there a less hacky solution?
    for i in range(8, len(code)+1, 8):
        m_byte = 0b00000000
        encoded_byte = code[i-8:i]
        # for char in encoded_byte:
        #     print("char: {} ord: {}".format(char, hex(ord(char))))

        for j in range(8):
            m_byte = m_byte >> 1
            if encoded_byte[j] == character_set[1]:
                m_byte = m_byte | 0b10000000
            elif encoded_byte[j] == character_set[0]:
                pass

        msg_bytes.append(m_byte)

    if binary:
        return bytes(msg_bytes)
    return bytes(msg_bytes).decode('utf-8')