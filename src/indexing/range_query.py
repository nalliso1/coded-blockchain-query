from coding.decoder import Decoder

class RangeQuery:
    def __init__(self, amvsl_index):
        self.amvsl_index = amvsl_index
        self.decoder = None  # Will be set when needed

    def execute(self, start_key, end_key):
        """Execute a range query between the start and end keys"""
        return self.amvsl_index.range_query(start_key, end_key)

    def execute_range_query(self, start_timestamp, end_timestamp):
        """Execute a range query based on timestamps"""
        results = []
        data = self.amvsl_index.range_query_by_timestamp(start_timestamp, end_timestamp)
        
        return data