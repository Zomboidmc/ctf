with open('digits.bin') as f:
    bits = f.read().strip()

# remove all whitespace/newlines
bits = ''.join(bits.split())

# pad to full byte
bits = bits.ljust((len(bits) + 7) // 8 * 8, '0')

# convert 8 bits at a time -- never the whole string at once
data = bytearray()
for i in range(0, len(bits), 8):
    byte_str = bits[i:i+8]
    data.append(int(byte_str, 2))

with open('output.jpeg', 'wb') as f:
    f.write(data)

print(f"Wrote {len(data)} bytes")
