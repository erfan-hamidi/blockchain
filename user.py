from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import hashlib
from transaction import Transaction
import random


class User:
    def __init__(self, name):
        self.name = name
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()
        self.transactions = []
        self.miner = []

    def create_transaction(self, receiver, text, user_rec):
        data = str(f"{self.public_key.export_key().decode()},{user_rec.public_key.export_key().decode()},{text}").encode()
        data_to_sign = SHA256.new(data)
        signer = pkcs1_15.new(self.private_key)
        signature = signer.sign(data_to_sign)
        print(self.public_key)
        v = pkcs1_15.new(self.public_key)
        v.verify(data_to_sign, signature)
        self.signature = signature
        transaction = Transaction(
            sender= self.name,
            receiver= receiver,
            text= text,
            publickey_sender= self.public_key.export_key().decode(),
            publickey_receviver= user_rec.public_key.export_key().decode(),
            hashtext= hashlib.sha256(text.encode()).hexdigest(),
            signature= self.signature
        )
        self.transactions.append(transaction)
        user_rec.transactions.append(transaction)
        miner = self.miner[random.randint(0,10)]
        miner.receive_transaction(transaction)
