import unittest
from src.indexing.range_query import RangeQuery
from src.indexing.amvsl import AMVSL

class TestRangeQuery(unittest.TestCase):

    def setUp(self):
        self.amvsl_index = AMVSL()
        self.range_query = RangeQuery(self.amvsl_index)

    def test_query_within_range(self):
        # Assuming we have a method to insert data into the AMVSL index
        self.amvsl_index.insert(data={"timestamp": 1, "value": "A"})
        self.amvsl_index.insert(data={"timestamp": 2, "value": "B"})
        self.amvsl_index.insert(data={"timestamp": 3, "value": "C"})
        
        result = self.range_query.execute(start=1, end=2)
        expected_result = [{"timestamp": 1, "value": "A"}, {"timestamp": 2, "value": "B"}]
        self.assertEqual(result, expected_result)

    def test_query_out_of_range(self):
        self.amvsl_index.insert(data={"timestamp": 1, "value": "A"})
        
        result = self.range_query.execute(start=2, end=3)
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_query_empty_index(self):
        result = self.range_query.execute(start=1, end=5)
        expected_result = []
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()