import requests

from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet

WALLET_RPC_PORT = 28888
WALLET_RPC_HOST = '127.0.0.1'
ORDER_ACCOUNT_INDEX = 1


def create_pay_address(label=None):

    wallet = Wallet(JSONRPCWallet(port=WALLET_RPC_PORT, host=WALLET_RPC_HOST))
    account = wallet.accounts[ORDER_ACCOUNT_INDEX]

    address = account.new_address(label=label)
    return str(address)

