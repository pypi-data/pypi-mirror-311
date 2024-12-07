import binascii
from typing import Union

from eth_typing import AnyAddress, ChecksumAddress, HexAddress
from eth_utils import hexstr_if_str, keccak, to_hex
from eth_utils.address import _HEX_ADDRESS_REGEXP

from checksum_dict._checksum import cchecksum


# this was ripped out of eth_utils and optimized a little bit


def to_checksum_address(value: Union[AnyAddress, str, bytes]) -> ChecksumAddress:
    """
    Makes a checksum address given a supported format.
    """
    norm_address_no_0x = to_normalized_address(value)[2:]
    address_hash = keccak(text=norm_address_no_0x)
    address_hash_hex_no_0x = binascii.hexlify(address_hash).decode("ascii")
    return ChecksumAddress(cchecksum(norm_address_no_0x, address_hash_hex_no_0x))


def to_normalized_address(value: Union[AnyAddress, str, bytes]) -> HexAddress:
    """
    Converts an address to its normalized hexadecimal representation.
    """
    try:
        hex_address = hexstr_if_str(to_hex, value).lower()
    except AttributeError:
        raise TypeError(f"Value must be any string, instead got type {type(value)}")

    if not is_address(hex_address):
        raise ValueError(
            f"Unknown format {repr(value)}, attempted to normalize to {repr(hex_address)}"
        )

    return hex_address


def is_address(value: str) -> bool:
    return _HEX_ADDRESS_REGEXP.fullmatch(value) is not None
