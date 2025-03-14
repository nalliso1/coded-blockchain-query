class AMVSL:
    def __init__(self):
        self.index = {}  # Key -> list of block_ids
        self.timestamp_index = {}  # timestamp -> list of (key, block_id) tuples

    def insert(self, key, value, block_id=None):
        """Insert a key with block_id (ignoring value for storage efficiency)"""
        if key not in self.index:
            self.index[key] = []
        
        # Only store block_id, not the value
        self.index[key].append(block_id)
        
        # If block_id contains timestamp information, we could index by that as well
        if block_id is not None and hasattr(block_id, 'timestamp'):
            timestamp = block_id.timestamp
            if timestamp not in self.timestamp_index:
                self.timestamp_index[timestamp] = []
            self.timestamp_index[timestamp].append((key, block_id))

    def retrieve(self, key):
        """Retrieve all block IDs for a key"""
        return self.index.get(key, [])

    def range_query(self, start_key, end_key):
        """Query all block IDs for keys in the specified range using numeric comparison"""
        result = []
        
        # Try to convert keys to integers for numeric comparison
        try:
            start_num = int(start_key)
            end_num = int(end_key)
            
            for key in self.index.keys():
                try:
                    key_num = int(key)
                    if start_num <= key_num <= end_num:
                        for block_id in self.index[key]:
                            result.append({"key": key, "block_id": block_id})
                except ValueError:
                    # Skip non-numeric keys
                    pass
        except ValueError:
            # Fall back to string comparison if conversion fails
            for key in sorted(self.index.keys()):
                if start_key <= key <= end_key:
                    for block_id in self.index[key]:
                        result.append({"key": key, "block_id": block_id})
        
        return result
    
    def range_query_by_timestamp(self, start_time, end_time):
        """Query all entries with timestamps in the specified range"""
        result = []
        for timestamp in sorted(self.timestamp_index.keys()):
            if start_time <= timestamp <= end_time:
                result.extend(self.timestamp_index[timestamp])
        return result