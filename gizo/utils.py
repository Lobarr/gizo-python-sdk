"""Helper functions provided by Gizo"""
import binascii
import base64

def b64_to_hex(value: str) -> str:
    """
    Parameters
    ----------
    value : str
        base64 encoded string

    Returns : str
    -------
    hex value of base64 encoded string
    """
    return bytes_to_hex(base64.b64decode(value))
def b64_to_bytes(value: str) -> list:
    """
    Parameters
    ----------
    value : str
        base64 encoded string

    Returns : str
    -------
    bytes list of base64 encoded string
    """
    return hex_to_bytes(b64_to_hex(value))
def bytes_to_hex(bytes_arr: bytes) -> str:
    """
    Paramerters
    -----------
    bytes_arr : list
        array of bytes

    Returns : str
    -------
    hex value of bytes array
    """
    return binascii.hexlify(bytearray(bytes_arr)).decode("utf-8")

def hex_to_bytes(value: str) -> list:
    """
    Parameters
    ----------
    value : str
        hex encoded string

    Returns : list
    -------
    bytes array of hex value
    """
    return list(binascii.unhexlify(value))
    