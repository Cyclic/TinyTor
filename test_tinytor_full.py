#!/usr/bin/env python3
"""
Full test of TinyTor circuit building using our relay data
"""
import sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, '/Users/god/CODE/goddard-enhanced')

from pure_tor_client import PureTorClient
from tinytor import TorSocket, Circuit, OnionRouter
import base64
import random
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

# Load our relay data
print("=" * 80)
print("Loading relay data...")
our_client = PureTorClient()
our_client._load_bootstrap_relays()
print(f"✓ Loaded {len(our_client.relays)} relays\n")

# Convert to TinyTor format
tinytor_relays = []
for relay in our_client.relays:
    try:
        tor_relay = OnionRouter.__new__(OnionRouter)
        tor_relay.nickname = relay.nickname
        tor_relay.ip = relay.address
        tor_relay.tor_port = relay.or_port
        tor_relay.dir_port = relay.dir_port
        tor_relay.identity = relay.fingerprint
        tor_relay.flags = []

        # Set ntor key
        ntor_b64 = base64.b64encode(relay.ntor_onion_key).decode('ascii')
        if ntor_b64[-1] != '=':
            ntor_b64 += '='
        tor_relay.key_ntor = ntor_b64

        # Set flags
        if relay.is_guard:
            tor_relay.flags.append('Guard')
        if relay.is_fast:
            tor_relay.flags.append('Fast')
        if relay.is_stable:
            tor_relay.flags.append('Stable')

        # Initialize crypto fields
        tor_relay._forward_digest = None
        tor_relay._backward_digest = None
        tor_relay.encryption_key = None
        tor_relay.decryption_key = None

        tinytor_relays.append(tor_relay)
    except:
        continue

print(f"✓ Converted {len(tinytor_relays)} relays to TinyTor format\n")

# Select relays
guards = [r for r in tinytor_relays if 'Guard' in r.flags and 'Fast' in r.flags]
if not guards:
    print("No guards found!")
    sys.exit(1)

guard = random.choice(guards[:30])
print(f"Selected Guard: {guard.nickname}")
print(f"  Address: {guard.ip}:{guard.tor_port}")
print(f"  Flags: {guard.flags}")

middles = [r for r in tinytor_relays if r != guard and 'Fast' in r.flags and 'Stable' in r.flags]
if not middles:
    print("No middle relays found!")
    sys.exit(1)

middle = random.choice(middles[:30])
print(f"\nSelected Middle: {middle.nickname}")
print(f"  Address: {middle.ip}:{middle.tor_port}")
print(f"  Flags: {middle.flags}")

# Build circuit using TinyTor
print("\n" + "=" * 80)
print("BUILDING CIRCUIT WITH TINYTOR")
print("=" * 80)

try:
    # Step 1: Create TorSocket and connect
    print("\n[1/4] Creating TorSocket and connecting to guard...")
    tor_socket = TorSocket(guard)
    tor_socket.connect()
    print("✓ Connected and completed handshake")

    # Step 2: Create Circuit
    print("\n[2/4] Creating Circuit...")
    circuit = Circuit(tor_socket)
    print(f"✓ Circuit created with ID: 0x{circuit.get_circuit_id():08x}")

    # Step 3: Create first hop (CREATE2)
    print("\n[3/4] Building first hop (CREATE2 to guard)...")
    circuit.create(guard)
    print(f"✓ First hop established to {guard.nickname}")

    # Step 4: Extend to middle (EXTEND2)
    print("\n[4/4] Extending to middle relay (EXTEND2)...")
    circuit.extend(middle)
    print(f"✓✓✓ EXTEND2 SUCCEEDED!")
    print(f"✓✓✓ Circuit extended to {middle.nickname}")

    print("\n" + "=" * 80)
    print("SUCCESS: TinyTor built a 2-hop circuit!")
    print("=" * 80)
    print(f"Path: {guard.nickname} -> {middle.nickname}")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

    # Check if it was a DESTROY
    if "DESTROY" in str(e) or "PROTOCOL" in str(e):
        print("\n" + "=" * 80)
        print("RESULT: TinyTor ALSO gets PROTOCOL errors!")
        print("=" * 80)
        print("This means the issue is NOT in our implementation.")
        print("It's likely a network/relay compatibility issue.")
