def cchecksum(str norm_address_no_0x, str address_hash_hex_no_0x) -> str:
    # Declare memoryviews for fixed-length data
    cdef unsigned char[::1] norm_address_mv = norm_address_no_0x.encode('ascii')
    cdef unsigned char[::1] hash_bytes_mv = address_hash_hex_no_0x.encode('ascii')
    
    # Create a buffer for our result
    # 2 for "0x" prefix and 40 for the address itself
    cdef unsigned char buffer[42]
    buffer[0] = b'0'
    buffer[1] = b'x'

    # Handle character casing based on the hash value
    cdef int i
    for i in range(40):
        if hash_bytes_mv[i] < 56:  # '0' to '7' have ASCII values 48 to 55
            buffer[i + 2] = norm_address_mv[i]
        else:
            buffer[i + 2] = norm_address_mv[i] & 0xDF  # Convert to uppercase

    return bytes(buffer).decode('ascii')
