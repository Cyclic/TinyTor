# TinyTor

A minimal Python implementation of the Tor protocol for educational purposes.

## Overview

TinyTor is a pure Python implementation of the Tor (The Onion Router) protocol. This project demonstrates how to build circuits through the Tor network using the NTOR handshake protocol.

## Features

- Pure Python implementation (no external Tor client required)
- NTOR handshake support for circuit building
- CREATE2 and EXTEND2 cell handling
- AES-CTR encryption for relay cells
- X25519 key exchange (Curve25519)
- HKDF-SHA256 key derivation

## Technical Details

This implementation includes:
- Connection to Tor directory authorities
- Parsing consensus documents
- Building multi-hop circuits through the Tor network
- NTOR cryptographic handshake (tor-spec.txt 5.1.4)
- Relay cell encryption/decryption with running digest verification

## Requirements

- Python 3.7+
- cryptography library

## Installation

```bash
pip install cryptography
```

## Usage

```python
from tinytor import TinyTor

# Create TinyTor instance
tor = TinyTor()

# Build a circuit
circuit = tor.create_circuit()

# Use the circuit for requests
# (See tinytor.py for full API)
```

## Protocol Implementation

This implementation follows the Tor protocol specifications:
- Link protocol version 4 (variable-length circuit IDs)
- NTOR handshake (RFC 5869 HKDF with Curve25519)
- Cell-based protocol (514-byte cells)
- AES-128-CTR for stream cipher
- SHA-1 for running digest computation

## Security Notice

⚠️ **This is an educational implementation.** It has not undergone security audits and should not be used for anonymity-critical applications. Use the official Tor Browser for actual anonymous browsing.

## Credits

Based on the TinyTor project with improvements to the NTOR handshake implementation and protocol compliance.

## License

Educational/Reference Implementation
