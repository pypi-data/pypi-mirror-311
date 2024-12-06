from .core.config import settings
import requests #type: ignore
from flowx_sdk.cli import FlowxCLI
from flowx_sdk.transaction import TransactionManager, Transaction
from flowx_sdk.wallets import Wallet

class Client:
    def __init__(self, api_key: str) -> None:
        self.flowx_cli = FlowxCLI()
        self.api_key = api_key
        self._base_url = settings.base_url
        self.authenticated = False #type: ignore

        # Initialize the http client (requests)
        self.session = requests.Session()

        # Attempt to authenticate on initialization
        self.authenticate()
    

    def authenticate(self):
        """Authenticate with the API using the provided API key."""
        self.flowx_cli.load_flowx_env()
        
        auth_url = f"{self._base_url}/verify-token/{self.api_key}"
        print(f"Authenticating with URL: {auth_url}")  # Debugging

        payload = {}
        headers = {'Authorization': f"Bearer {self.flowx_cli.get_access_token()}"} # Use X-Token header for authentication
        print(f"Headers: {headers}")  # Debugging


        # end a GET or POST request to verify the API key
        response = self.session.get(auth_url, headers=headers, data=payload)
        print(response.status_code)
        print(response)

        if response.status_code == 200:
            self.authenticated = True
            print("Authenticated successfully")
        else:
            self.authenticated = False
            print("Authentication failed 🌋 please check you API-Token ")

    def get_supported_currencies(self) -> str:
        supported_currencies = {
            "stablecoins": ["USDT", "USDC", "DAI", "BUSD", "EUROC"],
            "african_fiat": ["NGN", "KES", "ZAR", "GHS", "TZS", "UGX"],
            "global_fiat": ["USD", "EUR", "GBP"],
            "cryptocurrencies": ["SUI", "BTC", "ETH", "XRP"]
        }
        return str(supported_currencies)
    
    def send_payment(self, sender_wallet, reciever_wallet, amount, stablecoin) -> Transaction:
        
        transaction_manager = TransactionManager()
        new_transaction = transaction_manager.create_transaction(sender_wallet, reciever_wallet, amount, stablecoin)
        wallet = Wallet()
        wallet.send_fund(new_transaction)
        for index, transaction in enumerate(transaction_manager.list_transactions()):
            if new_transaction.transaction_id == transaction.transaction_id: #type: ignore
                transaction_manager.list_transactions()[index] = new_transaction #type: ignore
        return new_transaction

    def get_payment_status(self, payment_id) -> str:
        transaction_manager = TransactionManager()
        new_transaction = transaction_manager.create_transaction(Wallet.generate_wallet_address(), Wallet.generate_wallet_address(),10, "USDT")
        new_transaction.transaction_id = payment_id
        wallet = Wallet()
        wallet.send_fund(new_transaction)
        for transaction in transaction_manager.list_transactions():
            if new_transaction.transaction_id == payment_id:
                return transaction.status
        return "Transaction does not exist"