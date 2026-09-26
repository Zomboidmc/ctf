# Timestamped_Secrets
## Approach
* Looked at the encryption.py file
* Entire encryption algorithm is given
* the algo uses timestamp and sha256 key + aes-ecb for the encryption.
* The message.txt includes the timestamp around 1790147508

## Solution
* First derive the key from the timestamp by generating a sha256 hash of 1790147508
* taking only the first 16 bytes of the hash 
* since aes is a symmetrical key encryption algorithm, the same key can be used to decrypt it.
* the cryptohash is given in message.txt with unnecessary text. clean it and paste it in message.bin
* the cryptohash is now decrypted with the key using openssl command 
	openssl enc -aes-128-ecb -b -in message.bin -out decrypted.txt -K "" 
* The key is outputted

## Flag

```
academy{d0nt_trust_us3rs}
``` 

## Takeaway
* Carefully inspect the files given