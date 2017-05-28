from eth_connect import web3, get_contract


class OwnedTransactions(object):
    def __init__(self, pass_phrase, address_entity):
        self.pass_phrase = pass_phrase
        self.address_entity = address_entity
        self.contract_owned = get_contract("Owned", self.address_entity)

    def change_owner(self, new_owner):
        web3.personal.unlockAccount(web3.eth.coinbase, self.pass_phrase)

        self.contract_owned.transact(
            {'to': self.address_entity,
             'from': web3.eth.coinbase}
            ).changeOwner(new_owner)
        # transaction should be mined !

    def set_delegated_owner(self, new_delegated_owner):
        web3.personal.unlockAccount(web3.eth.coinbase, self.pass_phrase)

        self.contract_owned.transact(
            {'to': self.address_entity,
             'from': web3.eth.coinbase}
            ).setDelegatedOwner(new_delegated_owner)
        # transaction should be mined !

    def grant_access(self, address):
        web3.personal.unlockAccount(web3.eth.coinbase, self.pass_phrase)

        self.contract_owned.transact(
            {'to': self.address_entity,
             'from': web3.eth.coinbase}
            ).grantAccess(address)
        print address
        # transaction should be mined !

    def remove_access(self, address):
        web3.personal.unlockAccount(web3.eth.coinbase, self.pass_phrase)

        self.contract_owned.transact(
            {'to': self.address_entity,
             'from': web3.eth.coinbase}
            ).removeAccess(address)
        # transaction should be mined !

    def get_owner(self):
        try:
            return self.contract_owned.call().owner()
        except Exception:
            print 'owner is bad'

    def get_access(self, address):
        try:
            return self.contract_owned.call().hasAccess(address)
        except Exception:
            print 'cant get access'

