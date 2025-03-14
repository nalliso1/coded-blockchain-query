from blockchain.chain import Blockchain
from coding.encoder import Encoder
from coding.decoder import Decoder
from indexing.amvsl import AMVSL
from indexing.range_query import RangeQuery
from storage.distributed_store import DistributedStore
from storage.node_manager import NodeManager
import random
import time



def generate_sample_data(count=10, counter=0):
    """Generate sample key-value pairs for demonstration with zero-padded keys"""
    data = {}
    for i in range(count):
        x = counter+i
        key = f"{x:04d}"
        value = f"value_{random.randint(1000, 9999)}"
        data[key] = value
    return data

def main():
    # Initialize components
    blockchain = Blockchain()
    encoder = Encoder(block_size=1024, redundancy=2)
    decoder = Decoder(num_fragments=3, threshold=2)
    amvsl = AMVSL()
    range_query = RangeQuery(amvsl_index=amvsl) 
    node_manager = NodeManager(base_port=5000)
    distributed_store = DistributedStore(node_manager)


    print("Coded Blockchain Range Query Application Initialized.")
    
    # Generate and add blocks to the blockchain
    print("\n=== Adding blocks to blockchain ===")
    blocks = []
    counter = 2000
    for i in range(20):
        data = generate_sample_data(5,counter)
        print(f"Creating block {i} with data: {data}")
        block = blockchain.create_block(data)
        blocks.append(block)
        counter -= 100
    
    # Encode blocks and distribute fragments
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
    
    # Build index from blockchain data
    print("\n=== Building AMVSL index ===")
    for block in blockchain.get_blocks():
        for key, value in block.data.items():
            amvsl.insert(key, value, block.index)
    
    # Perform range queries
    print("\n=== Executing range queries ===")
    results = range_query.execute("102", "500")
    print(f"Range query metadata results: {results}")
    
    # Demonstrate data retrieval and decoding
    print("\n=== Retrieving and decoding data for matching blocks ===")
    
    # Extract unique block IDs from range query results
    unique_block_ids = set()
    for result in results:
        if 'block_id' in result:
            unique_block_ids.add(result['block_id'])
    
    print(f"Found data in {len(unique_block_ids)} blocks: {unique_block_ids}")
    
    for block_id in unique_block_ids:
        print(f"\nRetrieving data for block: {block_id}")
        
        keys_in_block = [result['key'] for result in results if result.get('block_id') == block_id]
        print(f"Keys to retrieve: {keys_in_block}")

        # Proper retrieval from correct nodes based on fragment distribution
        fragments = []
        # Try to retrieve fragments until we have enough
        for i in range(len(node_ids)):
            if len(fragments) < decoder.threshold:  # Stop once we have enough
                node_id = node_ids[i % len(node_ids)]
                print(f"Attempting to retrieve fragment {i} from node {node_id}...")
                fragment = distributed_store.retrieve(node_id, block_id, i)
                if fragment:
                    fragments.append(fragment)
                    print(f"Successfully retrieved fragment {i} from {node_id}")

        # After all retrieval attempts, check if we have enough to decode
        if len(fragments) >= decoder.threshold:
            recovered_data_str = decoder.decode(fragments)
            
            import ast
            recovered_data = ast.literal_eval(recovered_data_str)
            
            matching_data = {k: v for k, v in recovered_data.items() 
                           if k in keys_in_block}
            print(f"Retrieved key-value pairs from fragments: {matching_data}")
        else:
            print(f"Not enough fragments retrieved: {len(fragments)}/{decoder.threshold} required")
    
    print("\n=== Retrieved data successfully ===")

if __name__ == "__main__":
    main()