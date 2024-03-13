import time
import hashlib

class Transaction:
    def __init__(self, sender, receiver, text, public_key_sender, public_key_receviver, signature, hashtext):
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.timestamp = time.time()
        self.publickey_sender = public_key_sender,
        self.publickey_receviver = public_key_receviver,
        self.hashtext = hashlib.sha256(text.encode()).hexdigest(),
        self.signature = signature
        self.hashtext = hashtext