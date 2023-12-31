# stealth/stealth_meta_address.py


from ecdsa import SECP256k1, SigningKey
from hashlib import sha3_256
from .utils import point_from_hex, point_to_eth_addr

# Constants
N = 33  # Length of public key
FORMAT_PREFIX = "st:eth:0x"
META_ADDR_LEN = len(FORMAT_PREFIX) + 2 * 2 * N  # 2 * 2 = (spending + view) * (hex)
def generate_stealth_meta_address():
    # Generate spending key pair
    spending_private_key = SigningKey.generate(curve=SECP256k1)
    spending_public_key = spending_private_key.get_verifying_key()

    # Generate viewing key pair
    viewing_private_key = SigningKey.generate(curve=SECP256k1)
    viewing_public_key = viewing_private_key.get_verifying_key()

    # Convert public keys to hexadecimal format
    spending_pub_hex = spending_public_key.to_string('compressed').hex()
    viewing_pub_hex = viewing_public_key.to_string('compressed').hex()

    # Concatenate public keys to form stealth meta-address
    stealth_meta_address = f"st:eth:0x{spending_pub_hex}{viewing_pub_hex}"
    return stealth_meta_address, spending_private_key, viewing_private_key



def generate_stealth_address(sma):
    if len(sma) != META_ADDR_LEN or not sma.startswith(FORMAT_PREFIX):
        raise ValueError("Stealth Meta Address wrong length or prefix")

    # Generate ephemeral private key
    ephemeral_priv = SigningKey.generate(curve=SECP256k1)
    ephemeral_pub = ephemeral_priv.get_verifying_key()

    # Extract public keys from sma
    spend_pub_hex = sma[len(FORMAT_PREFIX):len(FORMAT_PREFIX) + 2 * N]
    view_pub_hex = sma[len(FORMAT_PREFIX) + 2 * N:]

    spend_pub = point_from_hex(spend_pub_hex)
    view_pub = point_from_hex(view_pub_hex)

    # Compute s and hash it
    s = ephemeral_priv.privkey.secret_multiplier * view_pub

    # Convert the point s to a byte string
    s_bytes = s.x().to_bytes(32, byteorder='big') + s.y().to_bytes(32, byteorder='big')
    s_hashed = sha3_256(s_bytes).digest()
    view_tag = s_hashed[0]

      # Compute public stealth address
    pub_s_hashed = int.from_bytes(s_hashed, byteorder='big') * SECP256k1.generator
    try:
        pub_stealth_address = spend_pub + pub_s_hashed
    except AssertionError:
        raise ValueError("Invalid public stealth address, not on curve")

    return {
        'stealth_address': point_to_eth_addr(pub_stealth_address),
        'ephemeral_pubkey': ephemeral_pub.to_string('compressed').hex(),
        'view_tag': view_tag
    }