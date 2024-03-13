import tkinter as tk
from tkinter import ttk
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

class User:
    def __init__(self, name):
        self.name = name
        self.private_key = RSA.generate(2048)  # Generate RSA private key
        self.public_key = self.private_key.publickey()
        self.miners = []  # List of connected miners
        self.transaction_keys = {}  # Dictionary to store symmetric keys for transactions

    def create_transaction(self, receiver, text):
        # Construct transaction
        transaction = {
            'sender': self.name,
            'receiver': receiver,
            'text': text
        }
        # Generate transaction hash
        transaction_hash = SHA256.new(str(transaction).encode())

        # Sign transaction hash with private key
        signer = pkcs1_15.new(self.private_key)
        signature = signer.sign(transaction_hash)

        # Encrypt transaction with symmetric key
        symmetric_key = b'\x00' * 16  # Dummy symmetric key
        encrypted_transaction = self.encrypt_transaction(transaction, symmetric_key)

        # Store symmetric key for transaction
        self.transaction_keys[transaction_hash] = symmetric_key

        return {
            'transaction': encrypted_transaction,
            'signature': signature,
            'hash': transaction_hash
        }

    def encrypt_transaction(self, transaction, symmetric_key):
        # Dummy encryption function, replace with actual symmetric encryption algorithm
        encrypted_transaction = transaction  # Placeholder for encryption
        return encrypted_transaction

    def send_message_to_miners(self, message):
        for miner in self.miners:
            miner.receive_message(message)

    def request_transaction_by_hash(self, hash):
        symmetric_key = self.transaction_keys.get(hash)
        if symmetric_key:
            # Decrypt and retrieve transaction
            decrypted_transaction = self.decrypt_transaction(hash, symmetric_key)
            return decrypted_transaction
        else:
            return None

    def decrypt_transaction(self, hash, symmetric_key):
        # Dummy decryption function, replace with actual symmetric decryption algorithm
        decrypted_transaction = self.transaction_keys[hash]  # Placeholder for decryption
        return decrypted_transaction
    

class Miner:
    def __init__(self, name):
        self.name = name
        self.blocks = []  # List of blocks

    def receive_message(self, message):
        # Dummy function to receive and record transactions
        self.create_block([message])

    def create_block(self, transactions):
        # Create a new block with the given transactions
        block = {
            'transactions': transactions
        }
        self.blocks.append(block)


def display_blocks():
    blocks_text.delete('1.0', tk.END)
    for i, block in enumerate(miner1.blocks):
        blocks_text.insert(tk.END, f"Block {i+1}\n")
        for transaction in block['transactions']:
            blocks_text.insert(tk.END, f"Transaction: {transaction}\n")
        blocks_text.insert(tk.END, "\n")

def submit_transaction():
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    text = text_entry.get()
    transaction_data = alice.create_transaction(receiver, text)
    alice.send_message_to_miners(transaction_data)
    status_label.config(text=f"Transaction from {sender} to {receiver} submitted successfully.")

def retrieve_transaction():
    hash_val = hash_entry.get()
    transaction = bob.request_transaction_by_hash(hash_val)
    if transaction:
        retrieved_text_label.config(text="Retrieved transaction: " + str(transaction))
    else:
        retrieved_text_label.config(text="Transaction not found.")

# Create instances
alice = User('Alice')
bob = User('Bob')
miner1 = Miner('Miner1')

# Connect users to miners
alice.miners.append(miner1)
bob.miners.append(miner1)

# GUI setup
root = tk.Tk()
root.title("Blockchain Simulation")
root.configure(background="#f0f0f0")

# Create styled frames
input_frame = ttk.Frame(root, padding="20")
input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

output_frame = ttk.Frame(root, padding="20")
output_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

# Input widgets
sender_label = ttk.Label(input_frame, text="Sender:")
sender_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
sender_entry = ttk.Entry(input_frame)
sender_entry.grid(row=0, column=1, padx=5, pady=5)

receiver_label = ttk.Label(input_frame, text="Receiver:")
receiver_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
receiver_entry = ttk.Entry(input_frame)
receiver_entry.grid(row=1, column=1, padx=5, pady=5)

text_label = ttk.Label(input_frame, text="Text:")
text_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
text_entry = ttk.Entry(input_frame)
text_entry.grid(row=2, column=1, padx=5, pady=5)

submit_button = ttk.Button(input_frame, text="Submit Transaction", command=submit_transaction)
submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

hash_label = ttk.Label(input_frame, text="Transaction Hash:")
hash_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
hash_entry = ttk.Entry(input_frame)
hash_entry.grid(row=4, column=1, padx=5, pady=5)

retrieve_button = ttk.Button(input_frame, text="Retrieve Transaction", command=retrieve_transaction)
retrieve_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Output widgets


status_label = ttk.Label(output_frame, text="")
status_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

retrieved_text_label = ttk.Label(output_frame, text="")
retrieved_text_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

blocks_text = tk.Text(output_frame, width=40, height=10)
blocks_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

display_blocks_button = ttk.Button(output_frame, text="Display Blocks", command=display_blocks)
display_blocks_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()

root.mainloop()
