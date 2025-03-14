from coding.decoder import Decoder

class RangeQuery:
    def __init__(self, amvsl_index):
        self.amvsl_index = amvsl_index

    def execute(self, start_key, end_key):
        """Execute range query on primary keys"""
        return self.amvsl_index.range_query(start_key, end_key)
        
    def execute_by_column(self, column, start_value, end_value):
        """Execute range query on a specific column"""
        return self.amvsl_index.range_query_by_column(column, start_value, end_value)