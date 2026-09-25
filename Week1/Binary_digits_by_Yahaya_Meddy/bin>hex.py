with open('digits.bin') as f:
    bits = f.read().strip()

# chunk into bytes and convert
chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
print(''.join(chars))
