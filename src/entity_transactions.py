from eth_connect import web3, get_contract
from ipfs_connect import add_to_ipfs, get_from_ipfs


class EntityTransactions(object):
    def __init__(self, pass_phrase, address_entity):
        self.pass_phrase = pass_phrase
        self.address_entity = address_entity
        self.contract_entity = get_contract("Entity", self.address_entity)

    def set_attribute(self, attribute_type, attribute_data):
        web3.personal.unlockAccount(web3.eth.coinbase, self.pass_phrase)

        self.contract_entity.transact(
            {'to': self.address_entity,
             'from': web3.eth.coinbase}
            ).setAttribute(attribute_type, attribute_data)
        # transaction should be mined !

    def get_attribute(self, attribute_id):
        try:
            return self.contract_entity.call().getAttribute(attribute_id)
        except Exception:
            print "can't get the attribute"
            return None

    def sign_attribute(self, attribute_id, timestamp_validity_end):
        web3.personal.unlockAccount(web3.eth.coinbase, self.pass_phrase)

        self.contract_entity.transact(
            {'to': self.address_entity,
             'from': web3.eth.coinbase}
            ).signAttribute(attribute_id, timestamp_validity_end)
        # transaction should be mined !

    def get_certificate(self, certificate_id):
        try:
            return self.contract_entity.call().certificates(certificate_id)
        except Exception:
            print "can't get the certificate"

    def revoke_signature(self, certificate_id):
        web3.personal.unlockAccount(web3.eth.coinbase, self.pass_phrase)

        self.contract_entity.transact(
            {'to': self.address_entity,
             'from': web3.eth.coinbase}
            ).revokeSignature(certificate_id)
        # transaction should be mined !

    def get_revocation(self, revocation_id):
        try:
            return self.contract_entity.call().revocations(revocation_id)
        except Exception:
            print "can't get the revocation"

    def set_attribute_ipfs(self, attribute_type, attribute_data_file):
        data_hash = add_to_ipfs(attribute_data_file)
        if data_hash is not None:
            self.set_attribute(self, attribute_type, data_hash)
        else:
            return None

    def get_attribute_ipfs(self, attribute_id):
        data_hash = self.get_attribute(self, attribute_id)
        if data_hash is not None:
            return get_from_ipfs(data_hash)
        else:
            return None
