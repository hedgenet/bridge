import boto3
import paramiko

from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet

from sshtunnel import SSHTunnelForwarder


class Payment:

    def __init__(
            self,
            ssh_key_bucket_name,
            ssh_key_object,
            daemon_host,
            daemon_username,
            daemon_port,
            order_account_index):

        print('inside the payment object')

        self.order_account_index = order_account_index

        # build SSH tunnel
        TMP_KEY_DESTINATION = '/tmp/hedgenet-admin.pem'

        s3_client = boto3.client('s3')
        s3_client.download_file(ssh_key_bucket_name, ssh_key_object, TMP_KEY_DESTINATION)

        pkey = paramiko.RSAKey.from_private_key_file(TMP_KEY_DESTINATION)

        server = SSHTunnelForwarder(
                daemon_host,
                ssh_username=daemon_username,
                ssh_pkey=pkey,
                remote_bind_address=('127.0.0.1', daemon_port)
                )

        print('will start the SSH tunnel')
        server.start()

        # Wallet
        self.wallet = Wallet(JSONRPCWallet(port=server.local_bind_port))

        print('Payment Object Ready !!! ')

        return

    def _pay_account(self):

        return self.wallet.accounts[self.order_account_index]

    def create_pay_address(self, label=None):
        account = self._pay_account()
        pay_address = account.new_address(label=label)

        self.wallet.refresh()
        return str(pay_address)

