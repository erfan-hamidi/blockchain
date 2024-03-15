from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
import json
import time
import hashlib
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
    def __init__(self, name, peers, public_key = None):
        self.name = name
        if public_key is not None:
            self.public_key = public_key
        else:
            self.private_key = RSA.generate(2048)
            self.public_key = self.private_key.publickey()
        self.blockchain = []
        self.memory_pool = []
        self.peers = peers

    def mine_block(self, index, previous_hash, block_time):
        timestamp = time.time()
        nonce = 0
        delta = 30
        # Calculate difficulty based on previous block mining time
        current_block_time = time.time() - block_time  # Assuming timestamp recorded
        difficulty = calculate_difficulty(delta, current_block_time)

        # Create a new block with the calculated difficulty
        

        block = Block(index, self.memory_pool, timestamp, previous_hash, nonce, self.name, difficulty)
        while True:
            block = Block(index, self.memory_pool, timestamp, previous_hash, nonce, self.name, difficulty)
            block_hash = block.hash
            if block_hash.startswith('0' * difficulty):  # Example difficulty level
                block.nonce = nonce
                self.replace_chain()
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
        signature = transaction.signature

        # Verify the signature using the public key and hash
        try:
            pkcs1_15.new(sender_public_key).verify(hash_obj, signature)
            return True  # Signature verification successful
        except (ValueError, TypeError, pkcs1_15.pkcs1_15Error):
            return False  # Signature verification failed


    def validate_transaction(self, transaction):
        
        # Example: Check if transaction signature is valid
        if not self.verify_signature(transaction):
            return False

        # Additional validation rules can be added here

        return True
    
    def gossip_transaction(self, transaction):
        for peer in self.peers:
            peer.receive_transaction(transaction)

    def gossip_block(self, block):
        for peer in self.peers:
            peer.receive_block(block)

    def validate_block(self, block):
        block_hash = Block.hash
        if not block_hash.startswith('0' * block.difficulty) and block_hash != hashlib.sha256(block.data.encode()).hexdigest():
            return False

        for transaction in block.transactions:
            if not self.validate_transaction(transaction):
                return False

        if block.previous_hash != self.blockchain[-1].hash:
            return False

        return True    
    
    def replace_chain(self, new_blockchain):
        if len(new_blockchain) <= len(self.blockchain):
            return False

        for block in new_blockchain:
            if not self.validate_block(block):
                return False

        self.blockchain = [Block.from_dict(block) for block in new_blockchain]
        return True