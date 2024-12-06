# Wallet creation and management

import os
import requests #type: ignore
from flowx_sdk.transaction import Transaction

currencies = {
    "Stablecoins": [
        {"symbol": "USDT", "name": "Tether"},
        {"symbol": "USDC", "name": "USD Coin"},
        {"symbol": "DAI", "name": "MakerDAO’s decentralized stablecoin"},
        {"symbol": "BUSD", "name": "Binance USD"},
        {"symbol": "EUROC", "name": "Circle's Euro-backed stablecoin"}
    ],
    "Local African Currencies": [
        {"symbol": "NGN", "name": "Nigerian Naira"},
        {"symbol": "KES", "name": "Kenyan Shilling"},
        {"symbol": "ZAR", "name": "South African Rand"},
        {"symbol": "GHS", "name": "Ghanaian Cedi"},
        {"symbol": "TZS", "name": "Tanzanian Shilling"},
        {"symbol": "UGX", "name": "Ugandan Shilling"}
    ],
    "Global Reserve Currencies": [
        {"symbol": "USD", "name": "US Dollar"},
        {"symbol": "EUR", "name": "Euro"},
        {"symbol": "GBP", "name": "British Pound"}
    ],
    "Cryptocurrencies for Liquidity Bridging": [
        {"symbol": "SUI", "name": "Sui"},
        {"symbol": "BTC", "name": "Bitcoin"},
        {"symbol": "ETH", "name": "Ethereum"},
        {"symbol": "XRP", "name": "Ripple"}
    ]
}


class Wallet:
    
    def __init__(self):
        self.wallet_address = None
        self._balance = 1000
        self.currency_list = [
            "SUI/USDT",
            "SUI/USDC",
            "SUI/DAI",
            "SUI/BUSD",
            "SUI/EUROC",
            "BTC/USDT",
            "BTC/USDC",
            "BTC/DAI",
            "BTC/BUSD",
            "BTC/EUROC",
            "ETH/USDT",
            "ETH/USDC",
            "ETH/DAI",
            "ETH/BUSD",
            "ETH/EUROC",
            "XRP/USDT",
            "XRP/USDC",
            "XRP/DAI",
            "XRP/BUSD",
            "XRP/EUROC",
            ]
        
    @staticmethod
    def generate_wallet_address():
        """Generate a unique twallet address ."""
        return "0x" + os.urandom(32).hex()

    @staticmethod
    def supported_currencies():
        for category, items in currencies.items():
            for item in items:
                return f"    - {item['symbol']} ({item['name']})"
    
    def get_wallet_balance(self, currency):
        # fetch balanace of assets base on the stable coin
        return self._balance

    def send_fund(self, transaction: Transaction) -> Transaction:
        if self._balance > ( transaction.amount + transaction.transaction_charge):
            self._balance -=  self._balance + transaction.transaction_charge
            transaction.status = "successful"
            return transaction
        else:
            transaction.status = "unsuccessful"
            return transaction



