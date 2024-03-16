import tkinter as tk
from tkinter import ttk
import json
import time
from block import Block
from user import User
from miner import Miner



class App:

    def create_user(self):
        username = self.username_entry.get()
        user = User(username)
        user.miner = self.miners
        self.users.append(user)
        x = user.public_key.export_key().decode()
        self.status_label_user.config(text=f"User {username} created successfully.\n\n\nUser public key: \n{x}")


    def create_miner(self):
        username = self.minername_entry.get()
        miner = Miner(username, self.miners)
        miner.blockchain = self.miners[0].blockchain[:]
        self.miners.append(miner)
        self.status_label_miner.config(text=f"Miner {username} created successfully.")



    def submit_transaction(self):
        
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        text = self.amount_entry.get()
        x = None
        for user in self.users:
            if user.name == sender:
                for rec in self.users:
                    if rec.name == receiver:
                        x = rec
                    else:
                        x = user
                user.create_transaction(receiver, text, x)
                self.status_label.config(text=f"Transaction from {sender} to {receiver} submitted successfully.")



    def write_blocks_to_file(self, filename, blockchain):
        with open(filename, 'w') as file:
            for block in blockchain:
                file.write(json.dumps(block.__str__()) + '\n')
        self.status_label_miner.config(text=f"Blocks written to file: {filename}")

    def read_blocks_from_file(filename):
        blocks = []
        with open(filename, 'r') as file:
            for line in file:
                block_data = json.loads(line)
                block = Block(block_data['index'], block_data['transactions'], block_data['timestamp'],
                            block_data['previous_hash'], block_data['nonce'])
                blocks.append(block)
        return blocks

    def display_transactions(self):
        self.transaction_text.delete('1.0', tk.END)
        for user in self.users:
            self.transaction_text.insert(tk.END, f"Transactions for {user.name}:\n")
            for transaction in user.transactions:
                self.transaction_text.insert(tk.END, f"Sender: {transaction.sender}, Receiver: {transaction.receiver}, Amount: {transaction.text}\n")
            self.transaction_text.insert(tk.END, "\n")


    def updatelist(self, event):
            if self.miner_combobox != None:
                self.miner_combobox['values'] = [miner.name for miner in self.miners]

    def show_blockchain(self):
        for miner in self.miners:
            if miner.name == self.miner_combobox.get():
                self.tree.delete(*self.tree.get_children())
                self.write_blocks_to_file(f'{miner.name}blocks.txt', miner.blockchain)
                for block in miner.blockchain:
                    self.tree.insert("", "end", text=f"Block {block.index}",
                             values=(block.index, block.miner, block.transactions, block.timestamp, block.previous_hash, block.hash, block.nonce))

    def stop_miners(self):
        print('stop')
        for i in self.miners:
            i.stop_event()


    def __init__(self, root):
    # Create instances
        self.users = []
        self.miners = []
        num_miners = 10
        for i in range(num_miners):
            miner = Miner(f"Miner {i+1}", self.miners)
            self.miners.append(miner)
        self. miner_thread = []
        for i in self.miners:
            i.start()
        # self.miners[0].start()
        # self.miners[1].start()
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.tab_create_user = ttk.Frame(self.notebook)
        self.tab_create_user.pack(fill='both', expand=True)
        self.tab_view_transactions = ttk.Frame(self.notebook)
        self.tab_view_transactions.pack(fill='both', expand=True)
        self.tab_create_miner = ttk.Frame(self.notebook)
        self.tab_create_miner.pack(fill='both', expand=True )
        self.notebook.add(self.tab_create_user, text='Create User')
        self.notebook.add(self.tab_view_transactions, text='View Transactions')
        self.notebook.add(self.tab_create_miner, text='Create Miner')
        # Create styled frames in each tab
        self.input_frame_create_user = ttk.Frame(self.tab_create_user, padding="5")
        self.input_frame_create_user.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        self.output_frame_view_transactions = ttk.Frame(self.tab_view_transactions, padding="50")
        self.output_frame_view_transactions.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        self.input_frame_create_miner = ttk.Frame(self.tab_create_miner, padding="50")
        self.input_frame_create_miner.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        # Input widgets for creating user
        self.username_label = ttk.Label(self.input_frame_create_user, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.input_frame_create_user)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.create_user_button = ttk.Button(self.input_frame_create_user, text="Create User", command=self.create_user)
        self.create_user_button.grid(row=0, column=2, padx=5, pady=5)

        self.status_label_user = ttk.Label(self.input_frame_create_user, text="")
        self.status_label_user.grid(row=6, column=0, columnspan=2, padx=3, pady=3)

        #miner
        self.minername_label = ttk.Label(self.input_frame_create_miner, text="Minername:")
        self.minername_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.minername_entry = ttk.Entry(self.input_frame_create_miner)
        self.minername_entry.grid(row=0, column=1, padx=5, pady=5)

        
        self.create_miner_button = ttk.Button(self.input_frame_create_miner, text="Create Miner", command=self.create_miner)
        self.create_miner_button.grid(row=0, column=2, padx=5, pady=5)
        self.status_label_miner = ttk.Label(self.input_frame_create_miner, text="")
        self.status_label_miner.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Miner widgets
        self.miners_label = ttk.Label(self.input_frame_create_miner, text="Miner:")
        self.miners_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.miner_combobox = None
        self.miner_combobox = ttk.Combobox(self.input_frame_create_miner, values=[miner.name for miner in self.miners])
        
        self.miner_combobox.grid(row=5, column=1, padx=5, pady=5)
        self.miner_combobox.bind("<<ComboboxSelected>>", self.updatelist)
        self.mine_block_button = ttk.Button(self.input_frame_create_miner, text="Show Blockchain Miner", command=self.show_blockchain)
        self.mine_block_button.grid(row=5, column=2, padx=5, pady=5)

        self.mine_block_button = ttk.Button(self.input_frame_create_miner, text="Stop Mine", command=self.stop_miners)
        self.mine_block_button.grid(row=7, column=2, padx=5, pady=5)

        # self.Input widgets for submitting transaction
        self.sender_label = ttk.Label(self.output_frame_view_transactions, text="Sender:")
        self.sender_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.sender_entry = ttk.Entry(self.output_frame_view_transactions)
        self.sender_entry.grid(row=0, column=1, padx=5, pady=5)

        self.receiver_label = ttk.Label(self.output_frame_view_transactions, text="Receiver:")
        self.receiver_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.receiver_entry = ttk.Entry(self.output_frame_view_transactions)
        self.receiver_entry.grid(row=1, column=1, padx=5, pady=5)

        self.amount_label = ttk.Label(self.output_frame_view_transactions, text="Text:")
        self.amount_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(self.output_frame_view_transactions)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        self.submit_transaction_button = ttk.Button(self.output_frame_view_transactions, text="Submit Transaction", command=self.submit_transaction)
        self.submit_transaction_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.display_transactions_button = ttk.Button(self.output_frame_view_transactions, text="Display Transactions", command=self.display_transactions)
        self.display_transactions_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # self.Output widgets for viewing transactions
        self.transaction_text = tk.Text(self.output_frame_view_transactions, width=40, height=10, bg="#ffffff", fg="#000000", font=("Arial", 10))
        self.transaction_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # self.Output widget for displaying status
        self.status_label = ttk.Label(self.output_frame_view_transactions, text="")
        self.status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.tree = ttk.Treeview(self.input_frame_create_miner, columns=("Index", 'Miner', "Transactions", "Timestamp", "Previous Hash", "Hash", "Nonce"))
        self.tree.heading("#0", text="Block")
        self.tree.heading("Index", text="Index")
        self.tree.heading("Miner", text="Miner")
        self.tree.heading("Transactions", text="Transactions")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Previous Hash", text="Previous Hash")
        self.tree.heading("Hash", text="Hash")
        self.tree.heading("Nonce", text="Nonce")
        self.tree.column("#0", width=50)
        self.tree.column("Index", width=50)
        self.tree.column("Miner", width=50)
        self.tree.column("Transactions", width=140)
        self.tree.column("Timestamp", width=50)
        self.tree.column("Previous Hash", width=140)
        self.tree.column("Hash", width=140)
        self.tree.column("Nonce", width=50)

        self.tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        #self.update_blockchain()




if __name__ == "__main__":
    # GUI setup
    root = tk.Tk()
    root.title("Blockchain Simulation")
    app = App(root)
    root.mainloop()