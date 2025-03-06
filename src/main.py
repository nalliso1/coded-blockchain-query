from blockchain.chain import Blockchain
from coding.encoder import Encoder
from coding.decoder import Decoder
from indexing.amvsl import AMVSL
from indexing.range_query import RangeQuery
from storage.distributed_store import DistributedStore
from storage.node_manager import NodeManager
import random
import time

def generate_sample_data(count=10):
    """Generate sample key-value pairs for demonstration"""
    data = {}
    for i in range(count):
        key = f"key_{i}"
        value = f"value_{random.randint(1000, 9999)}"
        data[key] = value
    return data

def main():
    # Initialize components
    blockchain = Blockchain()
    encoder = Encoder(block_size=1024, redundancy=2)
    decoder = Decoder(num_fragments=3, threshold=1)
    amvsl = AMVSL()
    range_query = RangeQuery(amvsl_index=amvsl) 
    distributed_store = DistributedStore()
    node_manager = NodeManager()

    print("Coded Blockchain Range Query Application Initialized.")
    
    # 1. Generate and add blocks to the blockchain
    print("\n=== Adding blocks to blockchain ===")
    for i in range(3):
        data = generate_sample_data(5)
        print(f"Creating block {i} with data: {data}")
        block = blockchain.create_block(data)
        # blockchain.add_block(block)
    
    # 2. Encode blocks and distribute fragments
    print("\n=== Encoding and distributing blocks ===")
    for block in blockchain.get_blocks():
        print(f"Encoding block: {block.id}")
        fragments = encoder.encode(block.data)
        
        # Distribute fragments across nodes
        node_ids = node_manager.get_available_nodes()
        print(f"Distributing {len(fragments)} fragments across {len(node_ids)} nodes")
        for i, fragment in enumerate(fragments):
            node_id = node_ids[i % len(node_ids)]
            distributed_store.store(node_id, block.id, i, fragment)
    
    # 3. Build index from blockchain data
    print("\n=== Building AMVSL index ===")
    for block in blockchain.get_blocks():
        for key, value in block.data.items():
            amvsl.insert(key, value, block.id)
    
    # 4. Perform range queries
    print("\n=== Executing range queries ===")
    # Query for keys between "key_2" and "key_8"
    results = range_query.execute("key_2", "key_8")
    print(f"Range query results: {results}")
    
    # 5. Demonstrate data retrieval and decoding
    print("\n=== Retrieving and decoding data ===")
    # Get a random block to retrieve
    target_block = random.choice(blockchain.get_blocks())
    print(f"Retrieving data for block: {target_block.id}")
    
    # Retrieve fragments from storage
    fragments = []
    for i in range(decoder.threshold):  # Only need threshold number of fragments
        fragment = distributed_store.retrieve(node_ids[i], target_block.id, i)
        fragments.append(fragment)
    
    # Decode the fragments to recover the original data
    recovered_data = decoder.decode(fragments)
    print(f"Original data: {target_block.data}")
    print(f"Recovered data: {recovered_data}")
    
    print("\n=== Demonstration completed successfully ===")

if __name__ == "__main__":
    main()