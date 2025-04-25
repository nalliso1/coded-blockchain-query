class BPlusTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []  
        self.next = None    

class BPlusTree:
    def __init__(self, order=10):
        self.root = BPlusTreeNode(leaf=True)
        self.order = order  
    
    def insert(self, key, value):
        key = str(key)
        if len(self.root.keys) >= self.order:
            new_root = BPlusTreeNode(leaf=False)
            new_root.children = [self.root]
            self._split_child(new_root, 0)
            self.root = new_root
        
        self._insert_non_full(self.root, key, value)
    
    def _insert_non_full(self, node, key, value):
        if node.leaf:
            i = len(node.keys) - 1
            while i >= 0 and float(key) < float(node.keys[i]):
                i -= 1
            i += 1
            
            if i > 0 and i <= len(node.keys) and float(key) == float(node.keys[i-1]):
                if isinstance(node.children[i-1], list):
                    node.children[i-1].append(value)
                else:
                    node.children[i-1] = [node.children[i-1], value]
            else:
                node.keys.insert(i, key)
                node.children.insert(i, [value])
        else:
            i = len(node.keys) - 1
            while i >= 0 and float(key) < float(node.keys[i]):
                i -= 1
            i += 1
            
            #Checks   if child is full
            if len(node.children[i].keys) >= self.order:
                self._split_child(node, i)
                
                if float(key) > float(node.keys[i]):
                    i += 1
            
            self._insert_non_full(node.children[i], key, value)
    
    def _split_child(self, parent, child_index):
        child = parent.children[child_index]
        new_child = BPlusTreeNode(leaf=child.leaf)
        
        mid = len(child.keys) // 2
        
        new_child.keys = child.keys[mid:]
        
        if not child.leaf:
            new_child.children = child.children[mid:]
            child.children = child.children[:mid]
        else:
            new_child.children = child.children[mid:]
            new_child.next = child.next
            child.next = new_child
        
        child.keys = child.keys[:mid]
        
        parent_key = child.keys[mid-1] if not child.leaf else new_child.keys[0]
        
        parent.keys.insert(child_index, parent_key)
        parent.children.insert(child_index + 1, new_child)
    
    def _find_leaf(self, key):
        current = self.root
        while not current.leaf:
            i = 0
            while i < len(current.keys) and float(key) >= float(current.keys[i]):
                i += 1
            current = current.children[i]
        return current
    
    def retrieve(self, key):
        key = str(key)
        leaf = self._find_leaf(key)
        
        #Searching in the leaf
        for i, k in enumerate(leaf.keys):
            if float(k) == float(key):
                return leaf.children[i]
        return None
    
    def range_query(self, start_key, end_key):
        results = []

        start_key = str(start_key)
        end_key = str(end_key)
        
        leaf = self._find_leaf(start_key)
        
        i = 0
        while i < len(leaf.keys) and float(leaf.keys[i]) < float(start_key):
            i += 1
        
        while leaf:
            while i < len(leaf.keys):
                if float(leaf.keys[i]) <= float(end_key):
                    results.extend(leaf.children[i])
                    i += 1
                else:
                    return results
            
            leaf = leaf.next
            i = 0
            
            if not leaf:
                break
        
        return results