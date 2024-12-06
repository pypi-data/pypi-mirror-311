import hashlib
import os
import requests #type: ignore

class Transaction:
    transaction_id = None
    
    def __init__(self, sender_wallet, reciever_wallet, amount, stablecoin):
        self.transaction_id = self._generate_transaction_id()
        self.sender_wallet = sender_wallet
        self.receiver_wallet = reciever_wallet
        self.amount = amount
        self.stablecoin = stablecoin,
        self.transaction_charge = 0.3
        self.status = "pending"

    def __repr__(self):
        return (
                    f"Transaction(transaction_id='{self.transaction_id}', "
                    f"sender_wallet='{self.sender_wallet}', "
                    f"receiver_wallet='{self.receiver_wallet}', "
                    f"amount={self.amount}, status='{self.status}')"
                )
    

    
    def _generate_transaction_id(self):
        """Generate a unique transaction ID resembling a Sui wallet address."""
        random_data = os.urandom(16)  # Generate 16 bytes of random data
        transaction_id = hashlib.sha256(random_data).hexdigest()[:64]  # Create a 64-character hex string
        return transaction_id

    def send_payment(self, sender_wallet, receiver_wallet, amount, stablecoin="USDC"):
        """Send payment from one wallet to another."""
        self.transaction_id = self.generate_transaction_id() # Generate a Sui-style transaction ID and update the transaction ID
        print(f"Transaction ID: {self.transaction_id}")  # Debugging
        data = {
            "transaction_id": self.transaction_id,
            "sender": sender_wallet,
            "receiver": receiver_wallet,
            "amount": amount,
            "stablecoin": stablecoin
        }
        # response = requests.post(f'{self.network_url}/send_payment', json=data)
        # if response.status_code == 200:
        #     return response.json()  # Return transaction info
        # else:
        #     raise Exception("Failed to send payment")
        return self.transaction_id


    def get_transaction_status(self, tx_id):
        """Fetch the status of a transaction."""
        # response = requests.get(f'{self.network_url}/transaction/{tx_id}/status')
        # if response.status_code == 200:
        #     return response.json()  # Return transaction status
        # else:
        #     raise Exception("Failed to fetch transaction status")
        return "completed"


class TransactionManager:
    
    def __init__(self):
        self._transactions: list[Transaction] = [] # Strictly a list of Transaction objects

    def create_transaction(self, sender_wallet, receiver_wallet, amount, stablecoin="USDC") -> Transaction:
        transaction = Transaction(sender_wallet, receiver_wallet, amount, stablecoin)
        self.add_transaction(transaction)
        return transaction

    def add_transaction(self, transaction):
        """Add a transaction to the list if it's an instance of the Transaction class."""
        if not isinstance(transaction, Transaction):
            raise ValueError("Only instances of the Transaction class can be added.")
        self._transactions.append(transaction)
    
    def list_transactions(self) -> list[Transaction]:
        return self._transactions