# type: ignore
import binascii
from typing import TYPE_CHECKING, AnyStr, Type, TypeVar, Union, cast, overload

from eth_typing import AnyAddress, ChecksumAddress, HexAddress, HexStr
from eth_utils import (
    add_0x_prefix,
    hexstr_if_str,
    is_address,
    keccak,
    to_hex,
)

if TYPE_CHECKING:
    import brownie
    import y

    AnyAddressOrContract = TypeVar(
        "AddressOrContract", "AnyAddress", brownie.Contract, y.Contract
    )


class EthAddressKey(str):
    """
    Pass in an eth address to create a checksummed EthAddressKey.
    """

    def __new__(cls, value: Union[bytes, str]) -> str:
        if isinstance(value, bytes):
            converted_value = (
                value.hex()
                if type(value).__name__ == "HexBytes"
                else HexBytes(value).hex()
            )
        else:
            converted_value = add_0x_prefix(str(value))
        try:
            converted_value = to_checksum_address(converted_value)
        except ValueError:
            raise ValueError(f"'{value}' is not a valid ETH address") from None
        return super().__new__(cls, converted_value)


"""
This library was built to have minimal dependencies, to minimize dependency conflicts for users.
The following code was ripped out of eth-brownie on 2022-Aug-06.
A big thanks to the many maintainers and contributors for their valuable work!
"""


def to_bytes(val: Union[bool, bytearray, bytes, int, str]) -> bytes:
    """
    Equivalent to: `eth_utils.hexstr_if_str(eth_utils.to_bytes, val)` .

    Convert a hex string, integer, or bool, to a bytes representation.
    Alternatively, pass through bytes or bytearray as a bytes value.
    """
    if isinstance(val, bytes):
        return val
    elif isinstance(val, str):
        return hexstr_to_bytes(val)
    elif isinstance(val, bytearray):
        return bytes(val)
    elif isinstance(val, bool):
        return b"\x01" if val else b"\x00"
    elif isinstance(val, int):
        # Note that this int check must come after the bool check, because
        #   isinstance(True, int) is True
        if val < 0:
            raise ValueError(f"Cannot convert negative integer {val} to bytes")
        else:
            return to_bytes(hex(val))
    else:
        raise TypeError(f"Cannot convert {val!r} of type {type(val)} to bytes")


def hexstr_to_bytes(hexstr: str) -> bytes:
    if hexstr.startswith("0x") or hexstr.startswith("0X"):
        non_prefixed_hex = hexstr[2:]
    else:
        non_prefixed_hex = hexstr

    # if the hex string is odd-length, then left-pad it to an even length
    if len(hexstr) % 2:
        padded_hex = "0" + non_prefixed_hex
    else:
        padded_hex = non_prefixed_hex

    try:
        ascii_hex = padded_hex.encode("ascii")
    except UnicodeDecodeError:
        raise ValueError(
            f"hex string {padded_hex} may only contain [0-9a-fA-F] characters"
        )
    else:
        return binascii.unhexlify(ascii_hex)


class HexBytes(bytes):
    """
    HexBytes is a *very* thin wrapper around the python built-in :class:`bytes` class.

    It has these three changes:
        1. Accepts more initializing values, like hex strings, non-negative integers, and booleans
        2. Returns hex with prefix '0x' from :meth:`HexBytes.hex`
        3. The representation at console is in hex
    """

    def __new__(
        cls: Type[bytes], val: Union[bool, bytearray, bytes, int, str]
    ) -> "HexBytes":
        bytesval = to_bytes(val)
        return cast(HexBytes, super().__new__(cls, bytesval))  # type: ignore  # https://github.com/python/typeshed/issues/2630  # noqa: E501

    def hex(self) -> str:
        """
        Output hex-encoded bytes, with an "0x" prefix.

        Everything following the "0x" is output exactly like :meth:`bytes.hex`.
        """
        return "0x" + super().hex()

    @overload
    def __getitem__(self, key: int) -> int: ...

    @overload  # noqa: F811
    def __getitem__(self, key: slice) -> "HexBytes": ...

    def __getitem__(
        self, key: Union[int, slice]
    ) -> Union[int, bytes, "HexBytes"]:  # noqa: F811
        result = super().__getitem__(key)
        if hasattr(result, "hex"):
            return type(self)(result)
        else:
            return result

    def __repr__(self) -> str:
        return f"HexBytes({self.hex()!r})"


# And this was ripped out of eth_utils and optimized a little bit


_MATCH_LOWER = "01234567"


def to_checksum_address(value: Union[AnyAddress, str, bytes]) -> ChecksumAddress:
    """
    Makes a checksum address given a supported format.
    """
    norm_address_no_0x = to_normalized_address(value)[2:]
    address_hash = keccak(text=norm_address_no_0x)
    address_hash_hex_no_0x = binascii.hexlify(address_hash).decode("ascii")
    checksum_address = "".join(
        addr_char if hash_char in _MATCH_LOWER else addr_char.upper()
        for addr_char, hash_char in zip(norm_address_no_0x, address_hash_hex_no_0x)
    )
    return ChecksumAddress(f"0x{checksum_address}")


def to_normalized_address(value: Union[AnyAddress, str, bytes]) -> HexAddress:
    """
    Converts an address to its normalized hexadecimal representation.
    """
    try:
        hex_address = hexstr_if_str(to_hex, value).lower()
    except AttributeError:
        raise TypeError(f"Value must be any string, instead got type {type(value)}")
    if is_address(hex_address):
        return hex_address
    else:
        raise ValueError(
            f"Unknown format {repr(value)}, attempted to normalize to "
            f"{repr(hex_address)}"
        )
