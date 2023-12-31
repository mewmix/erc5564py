# ERC-5564 Python Implementation

## Unaudited, heavy WIP, use in production at own risk.

## Quick start

```python
# Imports
from erc5564py.stealth_meta_address import generate_stealth_meta_address, generate_stealth_address
from erc5564py.stealth_address import computeStealthAddress, computeStealthKey
from erc5564py.utils import point_from_hex
# Generate Stealth Meta-Address
stealth_meta_address, spending_private_key, viewing_private_key = generate_stealth_meta_address()

# Generate Stealth Address
stealth_address_data = generate_stealth_address(stealth_meta_address)
ephemeral_pub_key_hex = stealth_address_data['ephemeral_pubkey']

# Convert ephemeral public key hex to Point
ephemeral_pub_key = point_from_hex(ephemeral_pub_key_hex)

# Check if the stealth address belongs to the recipient
computeStealthAddress(ephemeral_pub_key, viewing_private_key, spending_private_key.get_verifying_key(), stealth_address_data['view_tag'])
# Compute Stealth Private Key
stealth_private_key = computeStealthKey(ephemeral_pub_key, viewing_private_key, spending_private_key)

print(f"Stealth PK: {stealth_private_key.hex()}, Stealth Meta Addres {stealth_meta_address}, Stealth Address Data: {stealth_address_data}")


```
