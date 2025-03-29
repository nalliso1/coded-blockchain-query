from .node_server import NodeServer

class NodeManager:
    def __init__(self, base_port=5000):
        self.nodes = {}
        self.base_port = base_port
        
        self.add_node("node_1")
        self.add_node("node_2")
        self.add_node("node_3")
        self.add_node("node_4")
        self.add_node("node_5")
        self.add_node("node_6")
        
        self._register_peers()
    
    def add_node(self, node_id):
        if node_id not in self.nodes:
            port = self.base_port + int(node_id.split('_')[1])
            node = NodeServer(node_id, port=self.base_port)
            node.start()
            self.nodes[node_id] = node
    
    def _register_peers(self):
        for node_id, node in self.nodes.items():
            for peer_id, peer in self.nodes.items():
                if node_id != peer_id:
                    node.add_peer(peer_id, peer.host, peer.port)
    
    def remove_node(self, node_id):
        if node_id in self.nodes:
            self.nodes[node_id].stop()
            del self.nodes[node_id]
    
    def get_nodes(self):
        return list(self.nodes.keys())
    
    def get_available_nodes(self):
        return list(self.nodes.keys())
    
    def get_node_url(self, node_id):
        if node_id in self.nodes:
            return self.nodes[node_id].get_url()
        return None