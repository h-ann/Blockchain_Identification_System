from web3 import Web3, HTTPProvider
import json
from solc import compile_source
import time

web3 = Web3(HTTPProvider('http://localhost:8082'))
source_code = open("c12e.sol", "r").read()
compiled_contracts = compile_source(source_code)


def get_contract(contract_name, contract_address):
    return web3.eth.contract(
        abi=compiled_contracts['<stdin>:%s' % contract_name]['abi'],
        address=contract_address)


class MyContractAddresses(object):
    def __init__(self, pass_phrase):
        self.pass_phrase = pass_phrase
        try:
            addresses = json.load(open('addresses.json'))
            #address_owned = addresses['owned']
            address_entity = addresses['entity']
        except IOError:
            #address_owned = self.deploy_contract("Owned")
            address_entity = self.deploy_contract("Entity")
            data = {
                #"owned": address_owned,
                "entity": address_entity
            }
            with open('addresses.json', 'w') as outfile:
                json.dump(data, outfile)
        finally:
            #self.address_owned = address_owned
            self.address_entity = address_entity

    def deploy_contract(self, contract_name):  # contract_name is {Owned, Entity}
        web3.personal.unlockAccount(web3.eth.coinbase, self.pass_phrase)
        my_owned = web3.eth.contract(
            abi=compiled_contracts['<stdin>:%s' % contract_name]['abi'],
            bytecode=compiled_contracts['<stdin>:%s' % contract_name]['bin'],
            bytecode_runtime=compiled_contracts['<stdin>:%s' % contract_name]['bin-runtime'],

        )

        trans_hash = my_owned.deploy(transaction={'from': web3.eth.coinbase, 'gas':5000000})
        trans_receipt = web3.eth.getTransactionReceipt(trans_hash)
        # wait until mained !!!!!!!!!
        while trans_receipt is None:
            trans_receipt = web3.eth.getTransactionReceipt(trans_hash)
            time.sleep(3)

        return trans_receipt['contractAddress']
