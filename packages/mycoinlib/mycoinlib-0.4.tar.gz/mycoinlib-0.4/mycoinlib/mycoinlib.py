from bitcoinlib.keys import HDKey
import blockcypher
import requests

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
    
    def current_price_btc(self):
        url = "https://blockchain.info/ticker"
        r = requests.get(url)
        data = r.json()
        usd = data.get('USD').get('last')
        return usd

    def usd_to_btc(self, amount: float):
        current_price = self.current_price_btc()
        btc_amount = amount / current_price
        formatted_btc_amount = format(btc_amount, ".6f")
        return formatted_btc_amount
    

