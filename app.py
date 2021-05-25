import json
from web3 import Web3
from web3.middleware import geth_poa_middleware


infura_url = 'https://kovan.infura.io/v3/ca7c01a5664f4398be3a3fa1983ea7c1'
web3 = Web3(Web3.HTTPProvider(infura_url))

web3.middleware_onion.inject(geth_poa_middleware, layer=0)

abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"tokenOwner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"internalType":"uint256","name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"internalType":"uint256","name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"internalType":"uint256","name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"internalType":"uint256","name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
contractAddress = '0x243906c2168FFa20dd98DA222972aFA47Cc2009e'

contract = web3.eth.contract(address=contractAddress, abi=abi)

alice = '0xe62E0A21D860034Bc77F7D316dB6e1d4e750af47'
privatekey = '16a7a91fc2f21eeefc3c9f828f8eac478ff568461bcd5aaa8260a84ba39ec589'
bob = '0x7cCF646439964a3139a1fb7Ce45d090270FdBEc3'


def balanceof(userAddress):
    balance = contract.functions.balanceOf(userAddress).call()
    print('balance :', web3.fromWei(balance, 'ether'))


def transfer(fromAddress, toAddress, amount):
    transaction = contract.functions.transfer(
        toAddress, amount*10**18).buildTransaction()
    transaction.update({'chainId': 42})
    transaction.update({'gas': 500000})
    transaction.update({'nonce': web3.eth.get_transaction_count(fromAddress)})
    transaction.update({'gasPrice': web3.toWei(5, 'gwei')})

    signed_tx = web3.eth.account.sign_transaction(transaction, privatekey)
    txn_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

    print(tx_hash, '/n')


def fetchContractDetails():
    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()

    print('name :', name, '\n', 'symbol :', symbol,
          '\n', 'decimals :', decimals, '\n', )


def totalSupply():
    totalSupply = contract.functions.totalSupply().call()
    print("total supply :", totalSupply)


fetchContractDetails()

balanceof('0xe62E0A21D860034Bc77F7D316dB6e1d4e750af47')

totalSupply()

#transfer(alice, bob, 10)
