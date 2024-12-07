import threading
from collections import defaultdict
from typing import Any, DefaultDict, Dict, Generic, Optional, Tuple

from checksum_dict import exceptions
from checksum_dict.base import AnyAddressOrContract, ChecksumAddressDict, T


_LocksDict = DefaultDict[AnyAddressOrContract, threading.Lock]


class ChecksumAddressSingletonMeta(type, Generic[T]):
    def __init__(self, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> None:
        super().__init__(name, bases, namespace)
        self.__instances: ChecksumAddressDict[T] = ChecksumAddressDict()
        self.__locks: _LocksDict = defaultdict(threading.Lock)
        self.__locks_lock: threading.Lock = threading.Lock()

    def __call__(self, address: AnyAddressOrContract, *args: Any, **kwargs: Any) -> T:  # type: ignore
        address = str(address)
        try:
            return self.__instances[address]
        except exceptions.KeyError:
            pass  # NOTE: passing instead of proceeding lets helps us keep a clean exc chain

        with self.__get_address_lock(address):
            # Try to get the instance again, in case it was added while waiting for the lock
            try:
                return self.__instances[address]
            except exceptions.KeyError:
                pass  # NOTE: passing instead of proceeding here lets us keep a clean exc chain

            instance = super().__call__(address, *args, **kwargs)
            self.__instances[address] = instance
        self.__delete_address_lock(address)
        return instance

    def __getitem__(self, address: AnyAddressOrContract) -> T:
        """Get the singleton instance for `address` from the cache."""
        return self.__instances[str(address)]

    def __setitem__(self, address: AnyAddressOrContract, item: T) -> None:
        """Set the singleton instance for `address` from the cache.

        You can use this if you need to implement non-standard init sequences.
        """
        address = str(address)
        with self.__get_address_lock(address):
            self.__instances[address] = item
        self.__delete_address_lock(address)

    def __delitem__(self, address: AnyAddressOrContract) -> None:
        del self.__instances[str(address)]

    def get_instance(self, address: AnyAddressOrContract) -> Optional[T]:
        return self.__instances.get(str(address))

    def delete_instance(self, address: AnyAddressOrContract) -> None:
        try:
            del self.__instances[str(address)]
        except KeyError:
            pass
        
    def __get_address_lock(self, address: AnyAddressOrContract) -> threading.Lock:
        """Makes sure the singleton is actually a singleton."""
        with self.__locks_lock:
            return self.__locks[address]

    def __delete_address_lock(self, address: AnyAddressOrContract) -> None:
        """No need to maintain locks for initialized addresses."""
        with self.__locks_lock:
            try:
                del self.__locks[address]
            except KeyError:
                pass
