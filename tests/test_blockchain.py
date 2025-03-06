import unittest
from src.blockchain.block import Block
from src.blockchain.chain import Blockchain

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()

    def test_create_block(self):
        block_data = "Test Block"
        previous_hash = "0"
        block = self.blockchain.create_block(block_data, previous_hash)
        
        self.assertEqual(block.index, 1)
        self.assertEqual(block.data, block_data)
        self.assertEqual(block.previous_hash, previous_hash)

    def test_add_block(self):
        block_data_1 = "First Block"
        block_data_2 = "Second Block"
        previous_hash = "0"
        
        self.blockchain.create_block(block_data_1, previous_hash)
        block_2 = self.blockchain.create_block(block_data_2, self.blockchain.get_last_block().hash)
        
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(block_2.data, block_data_2)
        self.assertEqual(block_2.previous_hash, self.blockchain.get_last_block().hash)

    def test_validate_chain(self):
        block_data = "Test Block"
        previous_hash = "0"
        self.blockchain.create_block(block_data, previous_hash)
        
        self.assertTrue(self.blockchain.validate_chain())

    def test_invalid_chain(self):
        block_data = "Test Block"
        previous_hash = "0"
        self.blockchain.create_block(block_data, previous_hash)
        
        # Manually tamper with the blockchain
        self.blockchain.chain[0].data = "Tampered Data"
        
        self.assertFalse(self.blockchain.validate_chain())

if __name__ == '__main__':
    unittest.main()