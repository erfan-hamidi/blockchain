from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
import json
import time
import hashlib
from block import Block
import threading
import random


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
      return min(int(difficulty_adjustment), 4)  # Limit maximum difficulty
  else:
      return max(1, int(1 / difficulty_adjustment))


class Miner(threading.Thread):
    def __init__(self, name, peers, public_key = None):
        super().__init__()
        self.name = name
        if public_key is not None:
            self.public_key = public_key
        else:
            self.private_key = RSA.generate(2048)
            self.public_key = self.private_key.publickey()
        self.blockchain = []
        self.memory_pool = []
        self.peers = peers
        self.delta = 30
        self.current_block = None
        block = Block(
                index=0,
                previous_hash="0000000000000000000000000000000000000000000000000000000000000000",
                transactions="None",
                timestamp=0,
                difficulty=1,  # Adjust difficulty as needed
                nonce=8,
                miner='GOD'
                )
        self.blockchain.append(block)
        self.stop = False
        self.not_mine = False

    def stop_event(self):
        self.stop = True

    def run(self):
        while True:
            if self.stop: break
            time.sleep(random.randint(5,45))  # Simulate mining time
            self.current_block = self.mine_block()
            if not self.not_mine:
                print(f"{self.name} mined block {self.current_block.index}")
            
            

    def mine_block(self):
        index = len(self.blockchain) + 1
        previous_hash = self.blockchain[-1].hash
        block_time = self.blockchain[-1].timestamp
        timestamp = time.time()
        nonce = 0
        # Calculate difficulty based on previous block mining time
        current_block_time = time.time() - block_time  # Assuming timestamp recorded
        if block_time == 0:
            current_block_time = self.delta - 1

        difficulty = 2

        #print(difficulty)
        # Create a new block with the calculated difficulty
        
        while True:
            block = Block(index, self.memory_pool[:], timestamp, previous_hash, nonce, self.name, difficulty)
            #print(f'hash:{block_hash} nonce: {nonce}')
            if block.hash.startswith('0' * difficulty):  # Example difficulty level
                self.gossip_block(block)
                self.blockchain.append(block)
                self.not_mine =False
                self.memory_pool.clear()
                return block
            nonce += 1
            if self.not_mine:
                break

    def receive_transaction(self, transaction):
        # Validate transaction
        val = self.validate_transaction(transaction)
        print(f'rev trx:{val},{self.name}')
        if val and transaction not in self.memory_pool:
            self.memory_pool.append(transaction)
            self.gossip_transaction(transaction)

    


    def verify_signature(self, transaction):
        # Get the public key of the sender
        #print(transaction.publickey_sender)
        sender_public_key = RSA.import_key(transaction.publickey_sender[0])

        # Construct the message to be hashed

        # Calculate the SHA256 hash of the message
        hash_obj = SHA256.new(transaction.val_sign())

        # Extract the signature from the transaction
        signature = transaction.signature
        
        #pub_key = RSA.importKey(sender_public_key)
        sign = pkcs1_15.new(sender_public_key)
        # Verify the signature using the public key and hash
        try:
            sign.verify(hash_obj, signature)
            return True  # Signature verification successful
        except ValueError :
            return False  # Signature verification failed


    def validate_transaction(self, transaction):
        
        # Example: Check if transaction signature is valid
        if not self.verify_signature(transaction):
            return False

        # Additional validation rules can be added here

        return True
    
    def gossip_transaction(self, transaction):
        for peer in self.peers:
            if peer.public_key == self.public_key:
                continue
            peer.receive_transaction(transaction)

    def gossip_block(self, block):
        for peer in self.peers:
            if peer.public_key == self.public_key:
                continue
            peer.receive_block(block)

    def receive_block(self, block):
        # Validate block
        val = self.validate_block(block)
        print(f'rev:{val},{self.name}')
        if val and block not in self.blockchain:
            self.blockchain.append(block)
            self.not_mine = True
            self.memory_pool = [transaction for transaction in self.memory_pool if transaction not in block.transactions]

    def validate_block(self, block):
        
        block_hash = block.hash
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