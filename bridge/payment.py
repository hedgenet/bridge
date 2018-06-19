import requests

from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet

WALLET_RPC_PORT = 28888
WALLET_RPC_HOST = '127.0.0.1'
ORDER_ACCOUNT_INDEX = 1

class Payment:

    def __init__(self, daemon_host, daemon_port, order_account_index):
        self.daemon_host = daemon_host
        self.daemon_port = daemon_port
        self.order_account_index = order_account_index

        # Create SSH tunnel for communication with monero daemon
        return

    def create_pay_address(self, label=None):





def create_pay_address(label=None):

    wallet = Wallet(JSONRPCWallet(port=WALLET_RPC_PORT, host=WALLET_RPC_HOST))
    account = wallet.accounts[ORDER_ACCOUNT_INDEX]

    address = account.new_address(label=label)
    return str(address)

