# Release Notes - TinyTor v1.0.0

## 🎉 Initial Release

This is the first stable release of TinyTor, a minimal pure Python implementation of the Tor protocol for educational purposes.

## ✨ Features

### Core Functionality
- **Pure Python Tor Client**: Complete implementation requiring no external Tor binaries
- **NTOR Handshake**: Fully functional NTOR (New Tor) cryptographic handshake protocol
- **Circuit Building**: Support for CREATE2 and EXTEND2 cells to build multi-hop circuits
- **Working Encryption**: AES-128-CTR stream cipher with proper counter management
- **Digest Verification**: SHA-1 running digest computation for relay cell integrity

### Protocol Support
- Link protocol version 4 (variable-length circuit IDs)
- Cell-based protocol (514-byte cells)
- X25519 (Curve25519) key exchange
- HKDF-SHA256 key derivation (RFC 5869)
- Server authentication verification
- Proper secret_input construction per tor-spec.txt

### Python 3.14 Compatibility
- Updated SSL implementation to use `SSLContext` instead of deprecated `ssl.wrap_socket()`
- Compatible with Python 3.7+ through Python 3.14

## 🔧 Technical Improvements

This release includes critical fixes to the NTOR handshake implementation:

1. **Correct `secret_input` Construction**
   - Properly builds: `EXP(Y,x) | EXP(B,x) | ID | B | X | Y | PROTOID`
   - Previously only used the two ECDH shared secrets

2. **Server Authentication Verification**
   - Validates server's AUTH response before deriving keys
   - Implements: `HMAC-SHA256(T_MAC, verify | ID | B | Y | X | PROTOID | "Server")`

3. **Correct KDF Info Parameter**
   - Uses only `M_EXPAND` in HKDF info parameter
   - Previously incorrectly included `relay_id`

4. **SSL Modernization**
   - Replaced deprecated `ssl.wrap_socket()` with `SSLContext`
   - Ensures compatibility with modern Python versions

## 🧪 Testing

Successfully tested with:
- Connection to Tor directory authorities
- Consensus document parsing
- CREATE2 handshake with guard relays
- EXTEND2 circuit extension to middle relays
- Multi-hop (3-hop) circuit building
- No PROTOCOL DESTROY errors

## 📦 Installation

```bash
pip install cryptography
```

## 🚀 Quick Start

```python
from tinytor import TinyTor

# Initialize TinyTor
tor = TinyTor()

# Build a circuit through the Tor network
circuit = tor.create_circuit()
```

## ⚠️ Security Notice

**This is an educational implementation.** It has not undergone security audits and should **NOT** be used for anonymity-critical applications. Use the official Tor Browser for actual anonymous browsing.

## 📚 References

- [Tor Protocol Specification](https://spec.torproject.org/)
- [RFC 5869 - HKDF](https://tools.ietf.org/html/rfc5869)
- [Curve25519](https://cr.yp.to/ecdh.html)

## 🙏 Credits

Based on the original TinyTor project by Marten4n6, with significant improvements to NTOR handshake implementation and protocol compliance.

## 📄 License

Educational/Reference Implementation

---

**Signed-off-by**: Cyclic ([@Cyclic](https://github.com/Cyclic))
**Release Date**: January 7, 2026
**Full Changelog**: Initial release (v1.0.0)
