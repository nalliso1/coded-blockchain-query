class BlockLocator:
    def __init__(self):
        self.index = {}  # Primary key index
        self.secondary_indices = {}  # Column indices

    def create_secondary_index(self, column_name):
        if column_name not in self.secondary_indices:
            self.secondary_indices[column_name] = {}
    
    def insert(self, key, value, block_id=None):
        if key not in self.index:
            self.index[key] = []
        self.index[key].append(block_id)
        
        if isinstance(value, dict):
            for column in self.secondary_indices:
                if column in value:
                    col_value = value[column]
                    if col_value not in self.secondary_indices[column]:
                        self.secondary_indices[column][col_value] = []
                    self.secondary_indices[column][col_value].append({
                        'key': key, 'block_id': block_id
                    })

    def retrieve(self, key):
        return self.index.get(key, [])

    def range_query_by_column(self, column, start_value, end_value):
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