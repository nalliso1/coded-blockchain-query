class AMVSL:
    def __init__(self):
        self.index = {}  # Primary key index
        self.secondary_indices = {}  # Column indices
        self.timestamp_index = {}  # timestamp -> list of (key, block_id) tuples

    def create_secondary_index(self, column_name):
        """Create index for a specific column"""
        if column_name not in self.secondary_indices:
            self.secondary_indices[column_name] = {}
    
    def insert(self, key, value, block_id=None):
        # Primary index
        if key not in self.index:
            self.index[key] = []
        self.index[key].append(block_id)
        
        # Update secondary indices
        if isinstance(value, dict):
            for column in self.secondary_indices:
                if column in value:
                    col_value = value[column]
                    if col_value not in self.secondary_indices[column]:
                        self.secondary_indices[column][col_value] = []
                    self.secondary_indices[column][col_value].append({
                        'key': key, 'block_id': block_id
                    })
        
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

    def range_query_by_column(self, column, start_value, end_value):
        """Query by column value range"""
        if column not in self.secondary_indices:
            return []
            
        results = []
        # Handle numeric and string types
        try:
            start_val = float(start_value)
            end_val = float(end_value)
            
            for value, entries in self.secondary_indices[column].items():
                try:
                    val = float(value)
                    if start_val <= val <= end_val:
                        results.extend(entries)
                except ValueError:
                    pass
        except ValueError:
            # String comparison
            for value, entries in self.secondary_indices[column].items():
                if start_value <= str(value) <= end_value:
                    results.extend(entries)
                    
        return results