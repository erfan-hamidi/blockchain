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