class DistributedStore:
    def __init__(self):
        # Map of node_id -> {block_id -> {fragment_id -> fragment_data}}
        self.storage = {}

    def store(self, node_id, block_id, fragment_id, fragment):
        """Store a fragment in the distributed storage"""
        if node_id not in self.storage:
            self.storage[node_id] = {}
        
        if block_id not in self.storage[node_id]:
            self.storage[node_id][block_id] = {}
        
        self.storage[node_id][block_id][fragment_id] = fragment
    
    def retrieve(self, node_id, block_id, fragment_id):
        """Retrieve a specific fragment from the distributed storage"""
        try:
            return self.storage[node_id][block_id][fragment_id]
        except KeyError:
            return None
    
    def store_fragment(self, node_id, fragment):
        """Legacy method for backward compatibility"""
        if node_id not in self.storage:
            self.storage[node_id] = {}
        # For simple fragment storage without block/fragment IDs
        if "fragments" not in self.storage[node_id]:
            self.storage[node_id]["fragments"] = []
        self.storage[node_id]["fragments"].append(fragment)
    
    def get_all_fragments_for_block(self, block_id):
        """Get all fragments for a specific block across nodes"""
        fragments = []
        for node_storage in self.storage.values():
            if block_id in node_storage:
                fragments.extend(node_storage[block_id].values())
        return fragments