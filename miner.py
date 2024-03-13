
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
        self.blocks = []  # List of mined blocks

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
