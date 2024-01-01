# stealth/utils.py

from ecdsa import SECP256k1
from ecdsa.ellipticcurve import Point
from Crypto.Hash import keccak



def point_to_eth_addr(point):
    # Converts an ECDSA point to an Ethereum address
    point_bytes = point.x().to_bytes(32, byteorder='big') + point.y().to_bytes(32, byteorder='big')
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(point_bytes)
    hash_bytes = keccak_hash.digest()
    return "0x" + hash_bytes[-20:].hex()

def point_from_hex(hex_str):
    # Converts a hex string to an ECDSA point
    # Check if the public key is compressed (02/03) or uncompressed (04)
    if hex_str.startswith("04"):
        # Uncompressed public key
        byte_array = bytes.fromhex(hex_str[2:])
        x_coord = int.from_bytes(byte_array[:32], byteorder='big')
        y_coord = int.from_bytes(byte_array[32:], byteorder='big')  
    elif hex_str.startswith("02") or hex_str.startswith("03"):
        # Compressed public key
        x_coord = int.from_bytes(bytes.fromhex(hex_str[2:]), byteorder='big')
        # Calculate y coordinate from x coordinate
        y_coord = decompress_y(x_coord, int(hex_str[:2], 16) % 2)
    else:
        raise ValueError("Invalid public key format")
    
    return Point(SECP256k1.curve, x_coord, y_coord, SECP256k1.order)

def decompress_y(x_coord, is_odd):
    # Decompress y coordinate from x coordinate
    # Elliptic curve equation: y^2 = x^3 + a*x + b
    curve = SECP256k1.curve
    y_squared = (x_coord**3 + curve.a() * x_coord + curve.b()) % curve.p()
    y_coord, _ = modular_sqrt(y_squared, curve.p())  # Get only one root

    # Ensure y_coord is not None
    if y_coord is None:
        raise ValueError("Invalid x coordinate for decompression")

    # Adjust y coordinate based on odd/even
    if (y_coord % 2) != is_odd:
        y_coord = curve.p() - y_coord

    return y_coord



def legendre_symbol(a, p):
    """
    Legendre symbol
    Define if a is a quadratic residue modulo p
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def modular_sqrt(a, p):
    """
    Tonelli-Shanks algorithm
    Find a quadratic residue (mod p) of a. That is, a number x satisfying
    x^2 = a mod p
    Return x or x and -x, otherwise return (None, None)
    """
    a %= p

    # Simple cases
    # (1) Find a non-quadratic residue (mod p)
    if legendre_symbol(a, p) != 1:
        return None, None

    # (2) Check simple case
    if p % 4 == 3:
        x = pow(a, (p + 1) // 4, p)
        return x, p-x

    # Factor p-1 on the form q * 2^s (with Q odd)
    q, s = p - 1, 0
    while q % 2 == 0:
        s += 1
        q //= 2

    # Select a non-square 'z' mod p
    z = 1
    while legendre_symbol(z, p) != -1:
        z += 1

    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while (t-1) % p != 0:
        i = min([j for j in range(1, m) if pow(t, 2**j, p) == 1])
        b = pow(c, 2**(m - i - 1), p)
        m, c, t, r = i, pow(b, 2, p), t * pow(b, 2, p) % p, r * b % p

    return r, p - r


