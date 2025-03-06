class AMVSL:
    def __init__(self):
        self.index = {}  # Key -> list of (value, block_id) tuples
        self.timestamp_index = {}  # timestamp -> list of (key, value, block_id) tuples

    def insert(self, key, value, block_id=None):
        """Insert a key-value pair with optional block_id"""
        if key not in self.index:
            self.index[key] = []
        
        entry = (value, block_id) if block_id is not None else (value, None)
        self.index[key].append(entry)
        
        # If block_id contains timestamp information, we could index by that as well
        if block_id is not None and hasattr(block_id, 'timestamp'):
            timestamp = block_id.timestamp
            if timestamp not in self.timestamp_index:
                self.timestamp_index[timestamp] = []
            self.timestamp_index[timestamp].append((key, value, block_id))

    def retrieve(self, key):
        """Retrieve all values for a key"""
        return self.index.get(key, [])

    def range_query(self, start_key, end_key):
        """Query all values for keys in the specified range"""
        result = []
        for key in sorted(self.index.keys()):
            if start_key <= key <= end_key:
                for value, block_id in self.index[key]:
                    result.append({"key": key, "value": value, "block_id": block_id})
        return result
    
    def range_query_by_timestamp(self, start_time, end_time):
        """Query all entries with timestamps in the specified range"""
        result = []
        for timestamp in sorted(self.timestamp_index.keys()):
            if start_time <= timestamp <= end_time:
                result.extend(self.timestamp_index[timestamp])
        return result