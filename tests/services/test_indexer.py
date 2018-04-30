import json
import pytest


@pytest.fixture()
def purchase_lib_contract(web3, wait_for_transaction, wait_for_block):
    contract_name = 'PurchaseLibrary'
    with open("./contracts/{}.json".format(contract_name)) as f:
            contract_interface = json.loads(f.read())
    wait_for_block(web3)

    PURCHASE_LIBRARY = {
        "abi": contract_interface['abi'],
        "bytecode": contract_interface['bytecode']
    }

    contract = web3.eth.contract(**PURCHASE_LIBRARY)
    deploy_txn_hash = contract.constructor().transact({'from': web3.eth.coinbase,
                                                       'gas': 1000000})
    deploy_receipt = wait_for_transaction(web3, deploy_txn_hash)
    contract_address = deploy_receipt['contractAddress']
    return contract(address=contract_address)


@pytest.fixture()
def listing_contract(web3, wait_for_transaction, wait_for_block, purchase_lib_contract):
    contract_name = 'Listing'
    with open("./contracts/{}.json".format(contract_name)) as f:
            contract_interface = json.loads(f.read())
    wait_for_block(web3)

    LISTING = {
        "abi": contract_interface['abi'],
        "bytecode": contract_interface['bytecode'].replace('__PurchaseLibrary_______________________', purchase_lib_contract.address)}

    contract = web3.eth.contract(**LISTING)
    deploy_txn_hash = contract.constructor().transact({'from': web3.eth.coinbase,
                                                       'gas': 1000000})
    deploy_receipt = wait_for_transaction(web3, deploy_txn_hash)
    contract_address = deploy_receipt['contractAddress']
    return contract(address=contract_address)



def test_new_listing_created(web3, wait_for_block, wait_for_transaction, listing_contract):
    print("+++++++++++++++++")
    print(listing_contract.__dict__)
