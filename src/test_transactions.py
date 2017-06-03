from entity_transactions import EntityTransactions
from owned_transactions import OwnedTransactions
from eth_connect import MyContractAddresses, get_contract, compiled_contracts
from ipfs_connect import add_to_ipfs, get_from_ipfs

# comment unnecessary transactions. test one by one. mine transactions during testing

my_entity_address = MyContractAddresses("Iam").address_entity
my_entity = EntityTransactions("Iam", my_entity_address)

# test ifps integration:

print add_to_ipfs('my_data.txt')
print get_from_ipfs('QmZpDc97Epm3ynoqNr2BDNbxEWwXMDrukBLB9BRVAyD9LL')

my_entity.set_attribute_ipfs('ipfsdata', 'my_data.txt')
my_entity.get_attribute_ipfs(0)

# set my attributes

my_entity.set_attribute("name", "Anna Hulita")
print my_entity.get_attribute(0)
my_entity.sign_attribute(0, 123465)
print my_entity.get_certificate(0)

# sign another user's attribute

another_entity_address = "0x7649e580b5ccc512586d6ad33b9131519c94b197"
another_entity = EntityTransactions("Iam", another_entity_address)
another_entity.sign_attribute(0, 123465)
print another_entity.get_certificate(0)

# revoke another user's attribute

another_entity.revoke_signature(0)
print another_entity.get_revocation(0)

# change access transactions manipulations

my_owned_address = MyContractAddresses("Iam").address_entity
my_owned = OwnedTransactions("Iam", my_owned_address)
my_owned.grant_access("0x6d6efa2ae4538e9a5e8df630524dfbe5961308a2")
print my_owned.get_access("0x6d6efa2ae4538e9a5e8df630524dfbe5961308a2")
my_owned.remove_access("0x6d6efa2ae4538e9a5e8df630524dfbe5961308a2")
my_owned.change_owner("0x6d775bfca75ebe226b15e1463ab7dd3466bb4a1b")
my_owned.set_delegated_owner("0x6d775bfca75ebe226b15e1463ab7dd3466bb4a1b")
