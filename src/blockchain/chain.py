from .block import Block
import time
import hashlib

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create genesis block
        genesis_block = Block(0, time.time(), {"genesis": "block"}, "0")
        self.chain.append(genesis_block)

    def create_block(self, data, previous_hash=None):
        if previous_hash is None and len(self.chain) > 0:
            previous_hash = self.chain[-1].hash
        
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=previous_hash or "0"
        )
        self.chain.append(block)
        return block
    
    def get_blocks(self):
        return self.chain
    
    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Check if the current block's previous hash matches the previous block's hash
            if current.previous_hash != previous.hash:
                return False
                
            # Check if the block's hash is valid
            if current.hash != current.calculate_hash():
                return False
                
        return True