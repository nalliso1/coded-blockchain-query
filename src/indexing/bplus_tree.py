class BPlusTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []  # For leaves: values; for internal nodes: child pointers
        self.next = None    # For leaf nodes to link to next leaf

class BPlusTree:
    def __init__(self, order=10):
        self.root = BPlusTreeNode(leaf=True)
        self.order = order  # Maximum number of children per node
    
    def insert(self, key, value):
        """Insert a key-value pair into the B+ tree"""
        # Convert key to string and then to float for consistent comparison
        key = str(key)
        # Handle root split case
        if len(self.root.keys) >= self.order:
            # Create new root
            new_root = BPlusTreeNode(leaf=False)
            # Make old root the first child of new root
            new_root.children = [self.root]
            # Split the old root and update the new root
            self._split_child(new_root, 0)
            # Set the new root
            self.root = new_root
        
        # Find leaf and insert
        self._insert_non_full(self.root, key, value)
    
    def _insert_non_full(self, node, key, value):
        """Insert into a node that is not full"""
        if node.leaf:
            # It's a leaf node, insert the key-value pair
            i = len(node.keys) - 1
            # Find position for new key
            while i >= 0 and float(key) < float(node.keys[i]):
                i -= 1
            i += 1
            
            # Insert key at position i
            if i > 0 and i <= len(node.keys) and float(key) == float(node.keys[i-1]):
                # Key exists, append value to existing values
                if isinstance(node.children[i-1], list):
                    node.children[i-1].append(value)
                else:
                    node.children[i-1] = [node.children[i-1], value]
            else:
                node.keys.insert(i, key)
                node.children.insert(i, [value])
        else:
            # It's an internal node, find the child to insert into
            i = len(node.keys) - 1
            while i >= 0 and float(key) < float(node.keys[i]):
                i -= 1
            i += 1
            
            # Check if child is full
            if len(node.children[i].keys) >= self.order:
                # Split the child
                self._split_child(node, i)
                # After split, the middle key is moved up, so we need to decide which child to go down
                if float(key) > float(node.keys[i]):
                    i += 1
            
            # Recursive insert
            self._insert_non_full(node.children[i], key, value)
    
    def _split_child(self, parent, child_index):
        """Split a child node and update the parent"""
        # Get the child to be split
        child = parent.children[child_index]
        # Create a new node that will be the right sibling
        new_child = BPlusTreeNode(leaf=child.leaf)
        
        # Calculate split point - middle for internal nodes, median for leaf
        mid = len(child.keys) // 2
        
        # Copy the latter half of keys to new child
        new_child.keys = child.keys[mid:]
        
        if not child.leaf:
            # If it's an internal node, also move children
            new_child.children = child.children[mid:]
            # Keep only the first half of children in original child
            child.children = child.children[:mid]
        else:
            # For leaf nodes, need to link the nodes for range queries
            # and copy all key-value pairs
            new_child.children = child.children[mid:]
            # Keep the median key in the leaf but also promote it to parent
            # Connect the leaf nodes
            new_child.next = child.next
            child.next = new_child
        
        # Truncate the keys in the original child
        child.keys = child.keys[:mid]
        
        # Move the middle key up to the parent (for internal nodes)
        # or copy the middle key (for leaf nodes)
        parent_key = child.keys[mid-1] if not child.leaf else new_child.keys[0]
        
        # Insert the middle key and the new child pointer into parent
        parent.keys.insert(child_index, parent_key)
        parent.children.insert(child_index + 1, new_child)
    
    def _find_leaf(self, key):
        """Find the leaf node that should contain the key"""
        current = self.root
        while not current.leaf:
            i = 0
            while i < len(current.keys) and float(key) >= float(current.keys[i]):
                i += 1
            current = current.children[i]
        return current
    
    def retrieve(self, key):
        """Retrieve a value for a given key"""
        key = str(key)
        leaf = self._find_leaf(key)
        
        # Search in the leaf
        for i, k in enumerate(leaf.keys):
            if float(k) == float(key):
                return leaf.children[i]
        return None
    
    def range_query(self, start_key, end_key):
        """Return all values with keys in the range [start_key, end_key]"""
        results = []
        # Convert keys for consistent comparison
        start_key = str(start_key)
        end_key = str(end_key)
        
        # Find the leaf containing the start key
        leaf = self._find_leaf(start_key)
        
        # Find the starting position
        i = 0
        while i < len(leaf.keys) and float(leaf.keys[i]) < float(start_key):
            i += 1
        
        # Collect values in range from all relevant leaf nodes
        while leaf:
            # Process current leaf
            while i < len(leaf.keys):
                if float(leaf.keys[i]) <= float(end_key):
                    results.extend(leaf.children[i])
                    i += 1
                else:
                    # We've hit a key beyond our range
                    return results
            
            # Move to next leaf node
            leaf = leaf.next
            i = 0
            
            # If no more leaves, we're done
            if not leaf:
                break
        
        return results