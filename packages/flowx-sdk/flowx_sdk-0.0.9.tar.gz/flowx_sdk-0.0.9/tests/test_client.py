from flowx_sdk.client import Client
from flowx_sdk.wallets import  Wallet
from flowx_sdk.transaction import Transaction

def test_init_client():
    client = Client(api_key="ab6d74b8d46d7f8952bad3f1e0388e41")
    assert client.authenticated is True

def test_send_funds():
    client = Client(api_key="ab6d74b8d46d7f8952bad3f1e0388e41")
    transaction = client.send_payment(Wallet.generate_wallet_address(), Wallet.generate_wallet_address(),10, "USDT")
    print(transaction)
    assert type(transaction)  is Transaction

def test_get_payment_status():
    client = Client(api_key="ab6d74b8d46d7f8952bad3f1e0388e41")
    status = client.get_payment_status("d0a9ac39a288581fb1db0fcc7c8e550435b4aa07a6e09b7037d00d0a4b7419fc")
    assert status == "successful"

def test_get_supported_currencies():
    client = Client(api_key="ab6d74b8d46d7f8952bad3f1e0388e41")
    supported_currencies = client.get_supported_currencies()
    print(supported_currencies)
    assert type(supported_currencies) is str