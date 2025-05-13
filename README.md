# Coded Blockchain Based Range Queries

This project implements a coded blockchain system that allows for efficient range queries on historical data. By utilizing error correction codes, the system reduces the storage requirements for nodes while maintaining the security and integrity of the blockchain.

## Overview

The coded blockchain architecture enables decentralized storage of coded fragments, allowing nodes to participate in the network without needing to store entire blocks. This approach not only minimizes storage costs but also enhances the scalability of blockchain applications.

## Features

- **Coded Storage**: Utilizes error correction codes to encode blocks, allowing nodes to store only fragments of data.
- **Range Queries**: Implements historical range queries across multiple nodes, enabling efficient data retrieval.
- **Authenticated Multi-Version Index**: Extends the AMVSL index for managing historical data in a secure manner.

## Project Structure

```
coded-blockchain-query
├── src
│   ├── blockchain          # Blockchain implementation
│   ├── coding              # Encoding and decoding logic
│   ├── indexing            # Indexing and querying functionality
│   └── storage             # Distributed storage management
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
