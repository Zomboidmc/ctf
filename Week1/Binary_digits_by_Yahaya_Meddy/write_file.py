with open('digits.bin') as f:
    bits = f.read().strip()

# pad to multiple of 8 if needed
bits = bits.ljust((len(bits) + 7) // 8 * 8, '0')

byte_arr = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
with open('output.bin', 'wb') as out:
    out.write(byte_arr)
