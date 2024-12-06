cdef str _MATCH_LOWER = "01234567"

def cchecksum(str norm_address_no_0x, str address_hash_hex_no_0x) -> str:
    cdef str checksum_address_no_0x = "".join(
        addr_char if hash_char in _MATCH_LOWER else addr_char.upper()
        for addr_char, hash_char in zip(norm_address_no_0x, address_hash_hex_no_0x)
    )
    return f"0x{checksum_address_no_0x}"
