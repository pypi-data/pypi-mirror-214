from bitcoinlib.keys import HDKey
import blockcypher
import requests
from eth_account import Account

class Mycoinlib:
    # BTC functions
    # create new BTC wallet
    def create_btc_wallet(self):
        key = HDKey(network='bitcoin')
        private_key = key.wif()
        public_key = key.public_hex
        info = {
            'private_key': private_key,
            'public_key': public_key,
            'wallet': key.address()
        }
        return info

    # retrieve current BTC price in USD
    def current_price_btc(self):
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url)
        data = r.json()
        usd = data.get('bitcoin').get('usd')
        return float(usd)

    # convert USD to BTC
    def usd_to_btc(self, amount: float):
        current_price = self.current_price_btc()
        btc_amount = amount / current_price
        formatted_btc_amount = format(btc_amount, ".6f")
        return float(formatted_btc_amount)
    
    # get confirmed balance of BTC wallet
    def get_confirmed_btc_balance(self, wallet: str):
        sats = blockcypher.get_total_balance(wallet)
        btc = blockcypher.from_base_unit(sats, 'btc')
        return float(btc)
    

    # ETHEREUM FUNCTIONS
    # create new ETH wallet
    def generate_eth_wallet(self):
        account = Account.create()
        private_key = account._private_key.hex()
        public_key = account.address
        info = {
            'private_key': private_key,
            'public_key': public_key
        }
        return info

    # retrieve current price of ETH
    def current_price_eth(self):
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        r = requests.get(url)
        data = r.json()
        usd = data.get('ethereum').get('usd')
        return float(usd)

    # convert USD to ETH
    def usd_to_eth(self, amount: float):
        current_price = self.current_price_eth()
        eth_amount = amount / current_price
        formatted_eth_amount = format(eth_amount, ".6f")
        return float(formatted_eth_amount)

    # get confirmed ETH balance of wallet
    def get_confirmed_eth_balance(self, wallet: str):
        url = f"https://api.blockcypher.com/v1/eth/main/addrs/{wallet}/balance"
        r = requests.get(url)
        data = r.json()
        wei = data.get('final_balance')
        eth = wei / 10**18 
        return float(eth)