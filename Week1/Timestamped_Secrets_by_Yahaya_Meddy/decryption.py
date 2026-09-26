import time
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def try_decrypt(timestamp: int, ciphertext: bytes):
    """Attempt decryption with a given timestamp. Returns plaintext or None."""
    key = sha256(str(timestamp).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        padded = cipher.decrypt(ciphertext)
        plaintext = unpad(padded, AES.block_size)
        return plaintext.decode()
    except (ValueError, UnicodeDecodeError):
        # Padding check failed, or decoded bytes aren't valid UTF-8 -> wrong key
        return None

def brute_force_decrypt(ciphertext_hex: str, center_timestamp: int, window: int = 300):
    """
    Try timestamps in [center_timestamp - window, center_timestamp + window].
    center_timestamp: your best guess (e.g. current time, or upload time).
    window: how many seconds before/after to search.
    """
    ciphertext = bytes.fromhex(ciphertext_hex)

    for offset in range(0, window + 1):
        for candidate in {center_timestamp - offset, center_timestamp + offset}:
            result = try_decrypt(candidate, ciphertext)
            if result is not None:
                return candidate, result

    return None, None


if __name__ == "__main__":
    ct = "1677f86f41155474ff5233bc79d0ec79ab610074d921fea1140a448f8c8329d9"
    guess = 1790147508  # or a known approximate time

    ts, pt = brute_force_decrypt(ct, guess, window=300)
    if pt is not None:
        print(f"Found timestamp: {ts}")
        print(f"Plaintext: {pt}")
    else:
        print("No matching timestamp found in the search window.")
