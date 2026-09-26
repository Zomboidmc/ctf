#!/usr/bin/env python3
"""
Simple offline dictionary attack against unsalted SHA-256 password hashes
dumped from users.db (CTF use).

Usage:
    python3 crack.py users.db rockyou.txt
"""

import sqlite3
import hashlib
import sys


def load_targets(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM users")
    # hash -> username (may be a list if hashes collide, unlikely here)
    targets = {}
    for username, pwhash in cur.fetchall():
        targets.setdefault(pwhash.lower(), []).append(username)
    conn.close()
    return targets


def crack(targets, wordlist_path):
    found = {}
    remaining = set(targets.keys())

    with open(wordlist_path, "r", encoding="latin-1", errors="ignore") as f:
        for i, line in enumerate(f):
            if not remaining:
                break
            candidate = line.rstrip("\n").rstrip("\r")
            if not candidate:
                continue
            h = hashlib.sha256(candidate.encode()).hexdigest()
            if h in remaining:
                for user in targets[h]:
                    found[user] = candidate
                    print(f"[+] CRACKED  {user:25s} : {candidate}")
                remaining.discard(h)
            if i % 500000 == 0 and i > 0:
                print(f"[.] {i} words tried, {len(remaining)} hashes remaining...")

    return found, remaining


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <users.db> <wordlist.txt>")
        sys.exit(1)

    db_path, wordlist_path = sys.argv[1], sys.argv[2]
    targets = load_targets(db_path)
    print(f"[*] Loaded {len(targets)} unique password hashes from {db_path}")

    found, remaining = crack(targets, wordlist_path)

    print("\n=== Results ===")
    print(f"Cracked: {len(found)} / {len(targets)} unique hashes")
    if remaining:
        print(f"Not found in wordlist ({len(remaining)}):")
        for h in remaining:
            print(f"  {h}  -> users: {targets[h]}")


if __name__ == "__main__":
    main()
