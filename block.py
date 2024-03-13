import hashlib

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce, miner, difficulty):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner = miner
        self.difficulty = difficulty
        # Secure block hash generation using SHA-256 and other header information
        data = str(self)
        self.hash = hashlib.sha256(data.encode()).hexdigest()
    def __str__(self):
        return f"""Block {self.index}, Previous Hash: {self.previous_hash}, Timestamp: {self.timestamp}, Difficulty: {self.difficulty}, Nonce: {self.nonce}, miner: {self.miner}, Transactions:
            {', '.join([str(tx) for tx in self.transactions])}"""