# Coded Blockchain Based Range Queries

This project implements a coded blockchain system that enables efficient range queries on historical data while reducing per-node storage. By using error correction codes and distributed indexing, the system provides fault tolerance, scalability, and practical support for querying data ranges without storing the full chain.

## 📚 Overview

The system fragments blockchain data using Reed-Solomon encoding and distributes coded fragments across nodes. This reduces storage requirements at each node by 60% while still allowing complete block reconstruction from a subset of fragments. A B+ tree index enables efficient range queries on block attributes without needing to scan the entire blockchain.

## 📄 Research Paper

For a detailed explanation of the system design, implementation, and evaluation, read our full [CS4545 Final Report](./CS4545_Final_Report.pdf).

## 🚀 Features

- **Coded Storage**: Uses Reed-Solomon codes to encode and distribute fragments with built-in redundancy.
- **Range Queries**: Supports efficient range lookups using a distributed B+ tree index.
- **Fault Tolerance**: Blocks can be reconstructed from any 3 out of 5 fragments (40% redundancy).
- **Distributed Architecture**: Nodes communicate via Flask-based REST APIs for fragment storage and retrieval.

## 🧱 Project Structure

```
coded-blockchain-query
├── src
│   ├── blockchain          # Blockchain core logic
│   ├── coding              # Reed-Solomon encoder/decoder
│   ├── indexing            # B+ tree for range queries
│   └── storage             # Node servers and distribution logic
├── tests                   # Unit tests for the project
├── requirements.txt        # Project dependencies
└── setup.py                # Setup script for the project
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```
python src/main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Authors

- :raised_hands: :raised_hands: **Team Brute-Force!!!** :raised_hands: :raised_hands:
- Brahmpreet Singh
- Nicholas Allison
- Dineth Mudugamuwa Hewage

## 📌 My Contributions

This project was developed collaboratively by our team of three for the CS4545 course. We all participated in the design discussions, system testing, and performance evaluation. 

I contributed to:
- Implementing the node server and node manager components
- Developed the system evaluation framework
- Created the data loading & preprocessing utilities
- Authoring the project report and documentation
