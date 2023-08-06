from bitcoinlib.keys import HDKey
import blockcypher
import requests
from eth_account import Account


class BTC:
    # Create new BTC wallet
    @staticmethod
    def create_wallet():
        key = HDKey(network='bitcoin')
        private_key = key.wif()
        public_key = key.public_hex
        info = {
            'private_key': private_key,
            'public_key': public_key,
            'wallet': key.address()
        }
        return info

    # retrieve current BTC price
    @staticmethod
    def current_price():
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise exception for non-2xx status codes
            data = r.json()
            usd = data.get('bitcoin').get('usd')
            return float(usd)
        except (requests.RequestException, ValueError, KeyError) as e:
            raise APIException("Failed to retrieve BTC price from the API.") from e

    # convert USD to BTC
    @staticmethod
    def usd_to_btc(amount: float):
        try:
            current_price = BTC.current_price()
            btc_amount = amount / current_price
            formatted_btc_amount = format(btc_amount, ".6f")
            return float(formatted_btc_amount)
        except APIException as e:
            raise APIException("Failed to convert USD to BTC.") from e

    # get confirmed BTC balance
    @staticmethod
    def get_confirmed_balance(wallet: str):
        try:
            sats = blockcypher.get_total_balance(wallet)
            btc = blockcypher.from_base_unit(sats, 'btc')
            return float(btc)
        except blockcypher.BlockcypherException as e:
            raise APIException("Failed to retrieve confirmed BTC balance.") from e


class ETH:
    # Create new ETH wallet
    @staticmethod
    def create_wallet():
        account = Account.create()
        private_key = account._private_key.hex()
        public_key = account.address
        info = {
            'private_key': private_key,
            'public_key': public_key
        }
        return info

    # retrieve current ETH price
    @staticmethod
    def current_price():
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise exception for non-2xx status codes
            data = r.json()
            usd = data.get('ethereum').get('usd')
            return float(usd)
        except (requests.RequestException, ValueError, KeyError) as e:
            raise APIException("Failed to retrieve ETH price from the API.") from e

    # convert USD to ETH
    @staticmethod
    def usd_to_eth(amount: float):
        try:
            current_price = ETH.current_price()
            eth_amount = amount / current_price
            formatted_eth_amount = format(eth_amount, ".6f")
            return float(formatted_eth_amount)
        except APIException as e:
            raise APIException("Failed to convert USD to ETH.") from e

    # get confirmed ETH balance
    @staticmethod
    def get_confirmed_balance(wallet: str):
        url = f"https://api.blockcypher.com/v1/eth/main/addrs/{wallet}/balance"
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise exception for non-2xx status codes
            data = r.json()
            wei = data.get('final_balance')
            eth = wei / 10 ** 18
            return float(eth)
        except (requests.RequestException, ValueError, KeyError) as e:
            raise APIException("Failed to retrieve confirmed ETH balance.") from e


class LTC:
    # Create new LTC wallet
    @staticmethod
    def create_wallet():
        key = HDKey(network='litecoin')
        private_key = key.wif()
        public_key = key.public_hex
        info = {
            'private_key': private_key,
            'public_key': public_key,
            'wallet': key.address()
        }
        return info

    # retrieve current price of LTC
    @staticmethod
    def current_price():
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"
            r = requests.get(url)
            r.raise_for_status()  # Raise exception for non-2xx status codes
            data = r.json()
            usd = data.get('litecoin').get('usd')
            return float(usd)
        except (requests.RequestException, ValueError, KeyError) as e:
            raise APIException("Failed to retrieve ETH price from the API.") from e

    # convert USD to LTC
    @staticmethod
    def usd_to_ltc(amount: float):
        try:
            current_price = LTC.current_price()
            ltc_amount = amount / current_price
            formatted_ltc_amount = format(ltc_amount, ".6f")
            return float(formatted_ltc_amount)
        except APIException as e:
            raise APIException("Failed to convert USD to LTC.") from e

    # get confirmed LTC balance
    @staticmethod
    def get_confirmed_balance(wallet: str):
        url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{wallet}/balance"
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise exception for non-2xx status codes
            data = r.json()
            balance = data.get('final_balance')
            ltc = balance / 100000000
            return float(ltc)
        except (requests.RequestException, ValueError, KeyError) as e:
            raise APIException("Failed to retrieve confirmed LTC balance.") from e


class APIException(Exception):
    pass