import tkinter as tk
from tkinter import ttk
import json
import time
from block import Block
from user import User
from miner import Miner



def create_user():
    username = username_entry.get()
    user = User(username)
    users.append(user)
    miner = Miner(username, user.public_key)
    miners.append(miner)
    x = user.public_key.export_key().decode()
    status_label_user.config(text=f"User {username} created successfully.\n\n\nUser public key: \n{x}")


def create_miner():
    username = minername_entry.get()
    miner = Miner(username)
    miners.append(miner)
    status_label_miner.config(text=f"Miner {username} created successfully.")



def submit_transaction():
    print(miners)
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    text = amount_entry.get()
    x = None
    for user in users:
        if user.name == sender:
            for rec in users:
                if rec.name == receiver:
                    x = rec
                else:
                    x = user
            user.create_transaction(receiver, text, x)
            status_label.config(text=f"Transaction from {sender} to {receiver} submitted successfully.")

def mine_block():
    for miner in miners:
        if miner.name == miner_combobox.get():
            index = len(blockchain) + 1
            previous_hash = blockchain[-1].hash
            block_time = blockchain[-1].timestamp
            new_block = miner.mine_block(index, [user.transactions for user in users], previous_hash, block_time)
            blockchain.append(new_block)
            write_blocks_to_file('blocks.txt')
            status_label_miner.config(text=f"Block mined successfully by {miner.name}.")

def write_blocks_to_file(filename):
    with open(filename, 'w') as file:
        for block in blockchain:
            file.write(json.dumps(block.__str__()) + '\n')
    status_label_miner.config(text=f"Blocks written to file: {filename}")

def read_blocks_from_file(filename):
    blocks = []
    with open(filename, 'r') as file:
        for line in file:
            block_data = json.loads(line)
            block = Block(block_data['index'], block_data['transactions'], block_data['timestamp'],
                          block_data['previous_hash'], block_data['nonce'])
            blocks.append(block)
    return blocks

def display_transactions():
    transaction_text.delete('1.0', tk.END)
    for user in users:
        transaction_text.insert(tk.END, f"Transactions for {user.name}:\n")
        for transaction in user.transactions:
            transaction_text.insert(tk.END, f"Sender: {transaction.sender}, Receiver: {transaction.receiver}, Amount: {transaction.text}\n")
        transaction_text.insert(tk.END, "\n")

# Create instances
users = []
miners = []
blockchain = []
transactions = [
]
genesis_block = Block(
    index=0,
    previous_hash="0000000000000000000000000000000000000000000000000000000000000000",
    transactions=transactions,
    timestamp=time.time(),
    difficulty=1,  # Adjust difficulty as needed
    nonce=0,
    miner='GOD'
)
blockchain.append(genesis_block)

# GUI setup
root = tk.Tk()
root.title("Blockchain Simulation")


# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create tabs
tab_create_user = ttk.Frame(notebook)
tab_create_user.pack(fill='both', expand=True)
tab_view_transactions = ttk.Frame(notebook)
tab_view_transactions.pack(fill='both', expand=True)
tab_create_miner = ttk.Frame(notebook)
tab_create_miner.pack(fill='both', expand=True )
notebook.add(tab_create_user, text='Create User')
notebook.add(tab_view_transactions, text='View Transactions')
notebook.add(tab_create_miner, text='Create Miner')
# Create styled frames in each tab
input_frame_create_user = ttk.Frame(tab_create_user, padding="5")
input_frame_create_user.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

output_frame_view_transactions = ttk.Frame(tab_view_transactions, padding="50")
output_frame_view_transactions.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

input_frame_create_miner = ttk.Frame(tab_create_miner, padding="50")
input_frame_create_miner.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

# Input widgets for creating user
username_label = ttk.Label(input_frame_create_user, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_entry = ttk.Entry(input_frame_create_user)
username_entry.grid(row=0, column=1, padx=5, pady=5)

create_user_button = ttk.Button(input_frame_create_user, text="Create User", command=create_user)
create_user_button.grid(row=0, column=2, padx=5, pady=5)

status_label_user = ttk.Label(input_frame_create_user, text="")
status_label_user.grid(row=6, column=0, columnspan=2, padx=3, pady=3)

#miner
minername_label = ttk.Label(input_frame_create_miner, text="Minername:")
minername_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
minername_entry = ttk.Entry(input_frame_create_miner)
minername_entry.grid(row=0, column=1, padx=5, pady=5)

create_miner_button = ttk.Button(input_frame_create_miner, text="Create Miner", command=create_miner)
create_miner_button.grid(row=0, column=2, padx=5, pady=5)

status_label_miner = ttk.Label(input_frame_create_miner, text="")
status_label_miner.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Miner widgets
miners_label = ttk.Label(input_frame_create_miner, text="Miner:")
miners_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
miner_combobox = ttk.Combobox(input_frame_create_miner, values=[miner.name for miner in miners])
miner_combobox.grid(row=5, column=1, padx=5, pady=5)

mine_block_button = ttk.Button(input_frame_create_miner, text="Mine Block", command=mine_block)
mine_block_button.grid(row=5, column=2, padx=5, pady=5)


# Input widgets for submitting transaction
sender_label = ttk.Label(output_frame_view_transactions, text="Sender:")
sender_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
sender_entry = ttk.Entry(output_frame_view_transactions)
sender_entry.grid(row=0, column=1, padx=5, pady=5)

receiver_label = ttk.Label(output_frame_view_transactions, text="Receiver:")
receiver_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
receiver_entry = ttk.Entry(output_frame_view_transactions)
receiver_entry.grid(row=1, column=1, padx=5, pady=5)

amount_label = ttk.Label(output_frame_view_transactions, text="Text:")
amount_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
amount_entry = ttk.Entry(output_frame_view_transactions)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

submit_transaction_button = ttk.Button(output_frame_view_transactions, text="Submit Transaction", command=submit_transaction)
submit_transaction_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

display_transactions_button = ttk.Button(output_frame_view_transactions, text="Display Transactions", command=display_transactions)
display_transactions_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Output widgets for viewing transactions
transaction_text = tk.Text(output_frame_view_transactions, width=40, height=10, bg="#ffffff", fg="#000000", font=("Arial", 10))
transaction_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Output widget for displaying status
status_label = ttk.Label(output_frame_view_transactions, text="")
status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()