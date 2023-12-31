import unittest
import json
from erc5564py.stealth_meta_address import generate_stealth_address
from erc5564py.stealth_address import computeStealthKey, checkStealthAddress
from erc5564py.utils import point_from_hex
from ecdsa import SigningKey, SECP256k1
import os

class TestExternalAccess(unittest.TestCase):

    def load_keys_from_file(self, filename):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(base_dir, filename)
        with open(file_path, 'r') as file:
            return json.load(file)

    def test_access_with_external_stealth_address(self):
        # Sample external data
        external_stealth_address = "0xaa524252f2cda33aad07ddd575f471b8dced080d"
        external_ephemeral_pub_key_hex = "030f1cfcc54efbf3bb255d814b3bc0afe61fde26dd35a934687f499efec1b6c9c5"

        # Load keys
        keys_data = self.load_keys_from_file('stealth_keys.json')
        spending_private_key = SigningKey.from_string(bytes.fromhex(keys_data['spending_private_key']), curve=SECP256k1)
        viewing_private_key = SigningKey.from_string(bytes.fromhex(keys_data['viewing_private_key']), curve=SECP256k1)

        # Convert external ephemeral public key hex to Point
        external_ephemeral_pub_key = point_from_hex(external_ephemeral_pub_key_hex)

        # Compute Stealth Private Key for the External Address
        stealth_private_key = computeStealthKey(external_ephemeral_pub_key, viewing_private_key, spending_private_key)
        self.assertIsNotNone(stealth_private_key)

        # Check if the external stealth address belongs to the recipient
        is_correct_address = checkStealthAddress(external_ephemeral_pub_key, viewing_private_key, spending_private_key.get_verifying_key(), view_tag_announcement="0xdb") # Replace None with the actual view tag if available
        print(f"Is Correct Address: {is_correct_address}")
        self.assertTrue(is_correct_address)

        # Additional check: Compute the stealth address using the stealth meta-address and compare it with the external one
        stealth_meta_address = keys_data['stealth_meta_address']
        generated_stealth_address_data = generate_stealth_address(stealth_meta_address)
        generated_stealth_address = generated_stealth_address_data['stealth_address']
        print(f"Generated Stealth Address: {generated_stealth_address}")
        print(f"External Stealth Address: {external_stealth_address}")
        self.assertEqual(generated_stealth_address, external_stealth_address)

if __name__ == '__main__':
    unittest.main()
