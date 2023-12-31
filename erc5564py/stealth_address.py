# stealth/stealth_address.py

from ecdsa.util import number_to_string
from hashlib import sha3_256
from ecdsa import SECP256k1
from .utils import point_to_eth_addr
def computeStealthAddress(ephemeral_pub_point, viewing_priv, spending_pub, view_tag_announcement):
    curve = SECP256k1.curve
    order = SECP256k1.order
    generator = SECP256k1.generator  # 

    # Compute shared secret
    shared_secret_point = ephemeral_pub_point * viewing_priv.privkey.secret_multiplier
    shared_secret_bytes = number_to_string(shared_secret_point.x(), order) + number_to_string(shared_secret_point.y(), order)
    shared_secret_hashed = sha3_256(shared_secret_bytes).digest()

    # Check view tag
    view_tag = shared_secret_hashed[0]
    if view_tag != view_tag_announcement:
        return False

    # Compute stealth public key
    hashed_secret_scalar = int.from_bytes(shared_secret_hashed, byteorder='big')
    stealth_pub_point = spending_pub.pubkey.point + (hashed_secret_scalar * generator)
    stealth_address = point_to_eth_addr(stealth_pub_point)  #

    return stealth_address




def computeStealthKey(ephemeral_pub_point, viewing_priv, spending_priv):
    curve = SECP256k1.curve
    order = SECP256k1.order

    # Compute shared secret
    shared_secret_point = ephemeral_pub_point * viewing_priv.privkey.secret_multiplier
    shared_secret_bytes = number_to_string(shared_secret_point.x(), order) + number_to_string(shared_secret_point.y(), order)
    shared_secret_hashed = sha3_256(shared_secret_bytes).digest()

    # Compute stealth private key
    hashed_secret_scalar = int.from_bytes(shared_secret_hashed, byteorder='big')
    stealth_priv_scalar = (hashed_secret_scalar + spending_priv.privkey.secret_multiplier) % order
    stealth_priv_key = number_to_string(stealth_priv_scalar, order)

    return stealth_priv_key


