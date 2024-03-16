import time
import hashlib

class Transaction:
    def __init__(self, sender, receiver, text, publickey_sender, publickey_receviver, signature, hashtext):
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.timestamp = time.time()
        self.publickey_sender = publickey_sender,
        self.publickey_receviver = publickey_receviver,
        self.hashtext = hashtext,
        self.signature = signature

    def __str__(self) -> str:
        return f''''sender': {self.sender}, 'receiver': {self.receiver}, 'text': {self.text}, 'publickey_sender': {self.publickey_sender[0]}, 'publickey_receviver': {self.publickey_receviver[0]}, hashtext': {self.hashtext}, 'signature': {self.signature}
        '''
    def val_sign(self):
        return str(f"{self.publickey_sender[0]},{self.publickey_receviver[0]},{self.text}").encode()