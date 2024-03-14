from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import hashlib
from transaction import Transaction


class User:
    def __init__(self, name):
        self.name = name
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()
        self.transactions = []

    def create_transaction(self, receiver, text, x):
        data_to_sign = SHA256.new(str(f"{self.public_key},{x},{text}").encode())

        signer = pkcs1_15.new(self.private_key)
        signature = signer.sign(data_to_sign)
        self.signature = signature.hex()
        transaction = Transaction(
            sender= self.name,
            receiver= receiver,
            text= text,
            publickey_sender= self.public_key,
            publickey_receviver= x.public_key,
            hashtext= hashlib.sha256(text.encode()).hexdigest(),
            signature= self.signature
        )
        self.transactions.append(transaction)
        x.transactions.append(transaction)
