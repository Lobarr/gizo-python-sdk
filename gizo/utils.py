import binascii

def to_hex(bytes_arr):
    return binascii.hexlify(bytearray(bytes_arr)).decode("utf-8")

def to_bytes(_hex):
    return list(binascii.unhexlify(_hex))