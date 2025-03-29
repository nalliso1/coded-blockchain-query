from blockchain.blockchain import Blockchain
from coding.encoder import Encoder
from coding.decoder import Decoder
from indexing.block_locator import BlockLocator
from storage.distributed_store import DistributedStore
from storage.node_manager import NodeManager
import random
import pandas as pd
import json

def load_data_from_csv(file_path, key_column=None, records_per_block=10):
    try:
        df = pd.read_csv(file_path)
        blocks_data = []
        
        for i in range(0, len(df), records_per_block):
            block_data = {}
            batch = df.iloc[i:i+records_per_block]
            
            for idx, row in batch.iterrows():
                if key_column:
                    key = f"{row[key_column]}"
                else:
                    key = f"{idx:04d}"

                block_data[key] = row.to_dict()
            
            blocks_data.append(block_data)
            
        return blocks_data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

def main():
    blockchain = Blockchain()
    encoder = Encoder(redundancy=2)  # 3 data + 2 parity = 5 total fragments
    decoder = Decoder(num_fragments=5, threshold=3)  # Need at least 3 fragments
    block_locator = BlockLocator() 
    node_manager = NodeManager(base_port=5000)
    distributed_store = DistributedStore(node_manager)
    
    print("\n=== Loading data from CSV ===")
    csv_path = "src/data/students.csv"
    blocks_data = load_data_from_csv(csv_path, key_column="id")
    
    print("\n=== Creating Blocks and Adding them to blockchain ===")
    for i, data in enumerate(blocks_data):
        if (i < 2):
            print(f"Creating block {i} with {len(data)} records")
        if ( i == 2):
            print("...")
        block = blockchain.create_block(data)
    
    # Encode blocks and distribute fragments
    print("\n=== Encoding and distributing blocks ===")
    node_ids = node_manager.get_available_nodes()
    if not node_ids:
        print("No available nodes for distribution!")
        return
    
    for block in blockchain.get_blocks():
        print(f"Encoding block: {block.index}")
        # Serialize the entire block
        block_serialized = json.dumps({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
        fragments = encoder.encode(block_serialized)
        
        print(f"Distributing {len(fragments)} fragments across {len(node_ids)} nodes")
        starting_node = block.index % len(node_ids)
        for i, fragment in enumerate(fragments):
            node_id = node_ids[(starting_node + i) % len(node_ids)]
            distributed_store.store(node_id, block.index, i, fragment)
    
    # Create secondary indices for columns to query
    block_locator.create_secondary_index("math.grade")
    
    # Building dictornary structure from blockchain data
    print("\n=== Building indices ===")
    for block in blockchain.get_blocks():
        for key, value in block.data.items():
            block_locator.insert(key, value, block.index)
    
    # Example: Range query by math grade (3.0 to 5.0 range)
    print("\n=== Executing grade range query ===")
    grade_results = block_locator.range_query_by_column("math.grade", 9.0, 11.0)
    print(f"Students with math grades 9.0 - 11.0: {len(grade_results)}")
    
    # Extract unique block IDs from results
    unique_block_ids = set()
    for result in grade_results:
        if 'block_id' in result:
            unique_block_ids.add(result['block_id'])
    
    print(f"\n=== Found matching students in {len(unique_block_ids)} blocks ===")
    
    # Retrieve each block and display matching students
    for block_id in unique_block_ids:
        print(f"\nRetrieving data for block: {block_id}")
        
        # Get keys in this block
        keys_in_block = [result['key'] for result in grade_results 
                        if result.get('block_id') == block_id]
        print(f"Student IDs to retrieve: {keys_in_block}")
        
        # Retrieve fragments from nodes using the same pattern as storage
        fragments = []
        starting_node = block_id % len(node_ids)  # Match the distribution pattern
        for i in range(len(node_ids)):
            if len(fragments) < decoder.threshold:
                fragment_id = i
                node_id = node_ids[(starting_node + i) % len(node_ids)]
                print(f"Attempting to retrieve fragment {fragment_id} from node {node_id}...")
                fragment = distributed_store.retrieve(node_id, block_id, fragment_id)
                if fragment:
                    fragments.append(fragment)
                    print(f"Successfully retrieved fragment {fragment_id} from {node_id}")
        
        # Decode if we have enough fragments
        if len(fragments) >= decoder.threshold:
            recovered_block_str = decoder.decode(fragments)
            recovered_block_dict = json.loads(recovered_block_str)
            
            # Reconstruct a Block object if needed
            from blockchain.blockchain import Block
            recovered_block = Block(
                index=recovered_block_dict["index"],
                timestamp=recovered_block_dict["timestamp"],
                data=recovered_block_dict["data"],
                previous_hash=recovered_block_dict["previous_hash"]
            )
            
            # Verify hash matches
            if recovered_block.hash == recovered_block_dict["hash"]:
                print(f"Block {recovered_block.index} integrity verified")
            
            # Display information about students that match our query
            for key in keys_in_block:
                if key in recovered_block.data:
                    student = recovered_block.data[key]
                    print(f"ID: {key}, Name: {student.get('name')}, Math Grade: {student.get('math.grade')}")
        else:
            print(f"Not enough fragments retrieved: {len(fragments)}/{decoder.threshold} required")

if __name__ == "__main__":
    main()