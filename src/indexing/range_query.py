class RangeQuery:
    def __init__(self, amvsl_index):
        self.amvsl_index = amvsl_index

    def execute_range_query(self, start_timestamp, end_timestamp):
        results = []
        for node in self.amvsl_index.get_nodes():
            coded_fragments = node.retrieve_coded_fragments(start_timestamp, end_timestamp)
            decoded_data = self.decode_fragments(coded_fragments)
            results.extend(decoded_data)
        return self.aggregate_results(results)

    def decode_fragments(self, coded_fragments):
        # Implement decoding logic using the Decoder class
        decoder = Decoder()
        return decoder.decode(coded_fragments)

    def aggregate_results(self, results):
        # Implement aggregation logic for the results
        return sorted(results, key=lambda x: x['timestamp'])  # Assuming results have a timestamp field