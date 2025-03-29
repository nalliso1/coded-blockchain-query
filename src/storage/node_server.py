from flask import Flask, request, jsonify
import threading
import time

class NodeServer:
    def __init__(self, node_id, host='127.0.0.1', port=5000):
        self.node_id = node_id
        self.host = host
        self.port = port + int(node_id.split('_')[1])  # Different port for each node
        self.app = Flask(f"node_{node_id}")
        self.storage = {}  # Local storage for fragments
        self.peers = {}  # Known peer nodes
        
        self._setup_routes()
        
        self.server_thread = None
    
    def _setup_routes(self):
        @self.app.route('/fragment/<block_id>/<fragment_id>', methods=['PUT'])
        def store_fragment(block_id, fragment_id):
            data = request.get_json()
            fragment = data.get('fragment')
            
            if block_id not in self.storage:
                self.storage[block_id] = {}
            
            self.storage[block_id][fragment_id] = fragment
            return jsonify({"status": "success", "node": self.node_id})
        
        @self.app.route('/fragment/<block_id>/<fragment_id>', methods=['GET'])
        def retrieve_fragment(block_id, fragment_id):
            if block_id in self.storage and fragment_id in self.storage[block_id]:
                return jsonify({
                    "status": "success",
                    "fragment": self.storage[block_id][fragment_id]
                })
            return jsonify({"status": "not_found"}), 404
    
    def start(self):
        def run_server():
            self.app.run(host=self.host, port=self.port)
        
        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"Node server {self.node_id} started on {self.host}:{self.port}")
        time.sleep(1)  # Give the server time to start
    
    def stop(self):
        pass
    
    def add_peer(self, node_id, host, port):
        self.peers[node_id] = {"host": host, "port": port}
    
    def get_url(self):
        return f"http://{self.host}:{self.port}"