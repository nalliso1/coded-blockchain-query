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
    node_manager = NodeManager(base_port=5000)
    distributed_store = DistributedStore(node_manager)


    print("Coded Blockchain Range Query Application Initialized.")
    
    # 1. Generate and add blocks to the blockchain
    print("\n=== Adding blocks to blockchain ===")
    blocks = []
    for i in range(3):
        data = generate_sample_data(5)
        print(f"Creating block {i} with data: {data}")
        block = blockchain.create_block(data)
        blocks.append(block)
    
    # 2. Encode blocks and distribute fragments
    print("\n=== Encoding and distributing blocks ===")
    node_ids = node_manager.get_available_nodes()
    if not node_ids:
        print("No available nodes for distribution!")
        return
    
    for block in blockchain.get_blocks():
        print(f"Encoding block: {block.index}")
        # Convert block data to bytes for encoding if needed
        data_str = str(block.data)
        fragments = encoder.encode(data_str)
        
        print(f"Distributing {len(fragments)} fragments across {len(node_ids)} nodes")
        for i, fragment in enumerate(fragments):
            node_id = node_ids[i % len(node_ids)]
            distributed_store.store(node_id, block.index, i, fragment)
    
    # 3. Build index from blockchain data
    print("\n=== Building AMVSL index ===")
    for block in blockchain.get_blocks():
        for key, value in block.data.items():
            amvsl.insert(key, value, block.index)
    
    # 4. Perform range queries
    print("\n=== Executing range queries ===")
    # Query for keys between "key_2" and "key_8"
    results = range_query.execute("key_2", "key_8")
    print(f"Range query results: {results}")
    
    # 5. Demonstrate data retrieval and decoding
    print("\n=== Retrieving and decoding data ===")
    if blockchain.get_blocks():
        # Get a block to retrieve (skip genesis block)
        target_block = blockchain.get_blocks()[1] if len(blockchain.get_blocks()) > 1 else blockchain.get_blocks()[0]
        print(f"Retrieving data for block: {target_block.index}")
        
        # Retrieve fragments from storage
        fragments = []
        for i in range(decoder.threshold):
            if i < len(node_ids):
                fragment = distributed_store.retrieve(node_ids[i], target_block.index, i)
                if fragment:
                    fragments.append(fragment)
        
        if len(fragments) >= decoder.threshold:
            # Decode the fragments to recover the original data
            recovered_data = decoder.decode(fragments)
            print(f"Original data: {target_block.data}")
            print(f"Recovered data: {recovered_data}")
        else:
            print(f"Not enough fragments retrieved: {len(fragments)}/{decoder.threshold} required")
    
    print("\n=== Demonstration completed successfully ===")

if __name__ == "__main__":
    main()