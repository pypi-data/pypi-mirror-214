from bitcoinlib.keys import HDKey
import blockcypher

class Mycoinlib:
    def create_wallet(self):
        key = HDKey(network='bitcoin')
        private_key = key.wif()
        public_key = key.public_hex

        info = {
            'private_key': private_key,
            'public_key': public_key,
            'wallet': key.address()
        }

        return info

    def check_transactions(self, wallet):
        transactions = blockcypher.get_address_details(wallet, coin_symbol='btc')
        return transactions

    def get_confirmed_balance(self, wallet):
        transactions = self.check_transactions(wallet)
        return transactions['final_balance']
