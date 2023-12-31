import unittest
from erc5564py.stealth_meta_address import generate_stealth_meta_address, generate_stealth_address
from erc5564py.stealth_address import checkStealthAddress, computeStealthKey
from erc5564py.utils import point_from_hex

class TestStealthAddress(unittest.TestCase):

    def test_compute_stealth_key(self):
        # Generate Stealth Meta-Address
        stealth_meta_address, spending_private_key, viewing_private_key = generate_stealth_meta_address()

        # Generate Stealth Address
        stealth_address_data = generate_stealth_address(stealth_meta_address)
        ephemeral_pub_key_hex = stealth_address_data['ephemeral_pubkey']

        # Convert ephemeral public key hex to Point
        ephemeral_pub_key = point_from_hex(ephemeral_pub_key_hex)

        # Check if the stealth address belongs to the recipient
        is_correct_address = checkStealthAddress(ephemeral_pub_key, viewing_private_key, spending_private_key.get_verifying_key(), stealth_address_data['view_tag'])
        self.assertTrue(is_correct_address)

        # Compute Stealth Private Key
        stealth_private_key = computeStealthKey(ephemeral_pub_key, viewing_private_key, spending_private_key)
        self.assertIsNotNone(stealth_private_key)

if __name__ == '__main__':
    unittest.main()
