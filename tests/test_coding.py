import unittest
from src.coding.encoder import Encoder
from src.coding.decoder import Decoder

class TestCoding(unittest.TestCase):

    def setUp(self):
        self.encoder = Encoder()
        self.decoder = Decoder()
        self.data = "Test data for encoding"
        self.coded_fragments = self.encoder.encode(self.data)

    def test_encoding(self):
        self.assertIsNotNone(self.coded_fragments)
        self.assertGreater(len(self.coded_fragments), 0)

    def test_decoding(self):
        decoded_data = self.decoder.decode(self.coded_fragments)
        self.assertEqual(decoded_data, self.data)

    def test_partial_decoding(self):
        # Simulate loss of some coded fragments
        partial_fragments = self.coded_fragments[:len(self.coded_fragments) // 2]
        with self.assertRaises(Exception):
            self.decoder.decode(partial_fragments)

if __name__ == '__main__':
    unittest.main()