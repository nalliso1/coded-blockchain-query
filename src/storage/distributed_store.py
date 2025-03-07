# src/storage/distributed_store.py
import requests

class DistributedStore:
    def __init__(self, node_manager):
        self.node_manager = node_manager
    
    def store(self, node_id, block_id, fragment_id, fragment):
        """Store fragment on a specific node using HTTP request"""
        node_url = self.node_manager.get_node_url(node_id)
        if not node_url:
            return False
        
        url = f"{node_url}/fragment/{block_id}/{fragment_id}"
        try:
            response = requests.put(url, json={"fragment": fragment})
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def retrieve(self, node_id, block_id, fragment_id):
        """Retrieve fragment from a specific node using HTTP request"""
        node_url = self.node_manager.get_node_url(node_id)
        if not node_url:
            return None
        
        url = f"{node_url}/fragment/{block_id}/{fragment_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get("fragment")
            return None
        except requests.RequestException:
            return None