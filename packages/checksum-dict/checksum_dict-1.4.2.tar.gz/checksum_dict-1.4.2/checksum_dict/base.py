from typing import TYPE_CHECKING, Dict, Iterable, Tuple, TypeVar, Union

from checksum_dict import exceptions
from checksum_dict._key import EthAddressKey

if TYPE_CHECKING:
    from checksum_dict._key import AnyAddressOrContract
else:
    from eth_typing import AnyAddress as AnyAddressOrContract


T = TypeVar("T")

_SeedT = Union[Dict[AnyAddressOrContract, T], Iterable[Tuple[AnyAddressOrContract, T]]]


class ChecksumAddressDict(Dict[EthAddressKey, T]):
    """
    A dict that maps addresses to objects.
    Will automatically checksum your provided address key when setting and getting values.
    If you pass in a `seed` dictionary, the keys will be checksummed and the values will be set.
    """

    def __init__(self, seed: _SeedT = None) -> None:
        self.__dict__ = self
        if isinstance(seed, dict):
            seed = seed.items()
        if isinstance(seed, Iterable):
            for key, value in seed:
                self[key] = value

    def __repr__(self) -> str:
        return f"ChecksumAddressDict({str(dict(self))})"

    def __getitem__(self, key: AnyAddressOrContract) -> T:
        try:
            # It is ~700x faster to perform this check and then skip the checksum if we find a result for this key
            return dict.__getitem__(self, key)
        except KeyError:
            # NOTE: passing instead of checksumming here lets us keep a clean exc chain
            pass

        try:
            return dict.__getitem__(self, EthAddressKey(key))
        except KeyError as e:
            raise exceptions.KeyError(*e.args) from e.__cause__

    def __setitem__(self, key: AnyAddressOrContract, value: T) -> None:
        if key in self:
            # It is ~700x faster to perform this check and then skip the checksum if we find a result for this key
            dict.__setitem__(self, key, value)
        else:
            dict.__setitem__(self, EthAddressKey(key), value)

    def _getitem_nochecksum(self, key: EthAddressKey) -> T:
        """
        You can use this method in custom subclasses to bypass the checksum ONLY if you know its already been done at an earlier point in your code.
        """
        return dict.__getitem__(self, key)

    def _setitem_nochecksum(self, key: EthAddressKey, value: T) -> None:
        """
        You can use this method in custom subclasses to bypass the checksum ONLY if you know its already been done at an earlier point in your code.
        """
        if not key.startswith("0x") or len(key) != 42:
            raise ValueError(f"'{key}' is not a valid ETH address")
        dict.__setitem__(self, key, value)
