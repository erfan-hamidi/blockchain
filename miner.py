from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import json
import time
from block import Block

def calculate_difficulty(target_block_time, current_block_time):
  """
  Calculates the difficulty based on the desired block time and the actual time taken to mine the previous block.

  Args:
      target_block_time: The desired time interval between blocks (in seconds).
      current_block_time: The time taken to mine the previous block (in seconds).

  Returns:
      An integer representing the difficulty level.
  """

  # Adjust difficulty based on the ratio of desired vs actual block time
  difficulty_adjustment = target_block_time / current_block_time

  # Increase difficulty if mining is too fast, decrease if it's too slow
  if difficulty_adjustment > 1:
      return min(int(difficulty_adjustment), 255)  # Limit maximum difficulty
  else:
      return max(1, int(1 / difficulty_adjustment))


class Miner:
    def __init__(self, name):
        self.name = name
        self.blockchain = []
        self.memory_pool = []
        self.peers = []

    def mine_block(self, index, transactions, previous_hash, block_time):
        timestamp = time.time()
        nonce = 0
        # Calculate difficulty based on previous block mining time
        current_block_time = time.time() - block_time  # Assuming timestamp recorded
        difficulty = calculate_difficulty(10, current_block_time)

        # Create a new block with the calculated difficulty
        

        block = Block(index, transactions, timestamp, previous_hash, nonce,self.name, difficulty)
        while True:
            block = Block(index, transactions, timestamp, previous_hash, nonce, self.name, difficulty)
            block_hash = block.hash
            if block_hash.startswith('0'):  # Example difficulty level
                block.nonce = nonce
                self.blocks.append(block)
                return block
            nonce += 1

    def receive_transaction(self, transaction):
        # Validate transaction
        if self.validate_transaction(transaction):
            self.add_transaction_to_memory_pool(transaction)
            self.gossip_transaction(transaction)

    def receive_block(self, block):
        # Validate block
        if self.validate_block(block):
            self.blockchain.append(block)
            self.memory_pool = [transaction for transaction in self.memory_pool if transaction not in block.transactions]
            self.gossip_block(block)


    def verify_signature(self, transaction):
        # Get the public key of the sender
        sender_public_key = self.transaction.publickey_sender

        # Construct the message to be hashed
        message = json.dumps(transaction, sort_keys=True).encode()

        # Calculate the SHA256 hash of the message
        hash_obj = SHA256.new(message)

        # Extract the signature from the transaction
        signature = transaction['signature']

        # Verify the signature using the public key and hash
        try:
            pkcs1_15.new(sender_public_key).verify(hash_obj, signature)
            return True  # Signature verification successful
        except (ValueError, TypeError, pkcs1_15.pkcs1_15Error):
            return False  # Signature verification failed


    def validate_transaction(self, transaction):
        # Check if required fields are present in the transaction
        if 'sender' not in transaction or 'receiver' not in transaction or 'text' not in transaction:
            return False
        
        # Example: Check if the sender has sufficient balance
        sender_balance = self.calculate_balance(transaction['sender'])
        if sender_balance < transaction['text']:
            return False

        # Example: Check if transaction signature is valid
        if not self.verify_signature(transaction):
            return False

        # Additional validation rules can be added here

        return True