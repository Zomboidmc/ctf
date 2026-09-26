"""
Static solver for the heartbleed.c challenge.
Decodes obf_bytes (XOR 0xAA) and computes the djb2 hash the binary expects.
"""

# obf_bytes as declared in the decompiled source
obf_bytes = [-61, -1, -56, -62, -110, -101, -117, -64, -128, -62, -60, -117, 0, 0, 0, 0]

# --- Step 1: normalize signed bytes to their unsigned (0-255) bit pattern ---
unsigned_bytes = [b & 0xFF for b in obf_bytes]

# --- Step 2: decode loop stops at the first 0x00 byte (matches make_secret) ---
XOR_KEY = 0xAA
secret_bytes = []
for b in unsigned_bytes:
    if b == 0:
        break
    secret_bytes.append(b ^ XOR_KEY)

secret = bytes(secret_bytes)
print("Decoded secret:", secret)

# --- Step 3: djb2 hash, matching hash()'s exact 64-bit wraparound behavior ---
MASK64 = 0xFFFFFFFFFFFFFFFF
h = 5381
for c in secret:
    h = (h * 33 + c) & MASK64

print("djb2 hash (unsigned 64-bit):", h)
