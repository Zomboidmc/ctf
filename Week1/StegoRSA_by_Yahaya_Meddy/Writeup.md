Description:
	A message has been encrypted using RSA. The public key is gone… but someone might have been careless with the private key. Can you recover it and decrypt the message? Download the [flag](https://challenge-files.cylabacademy.net/library/9158482a92a4408128c3c320458089d0e8c2c1d8d8120ddaaabdf90397e4cedb/flag.enc) and [image](https://challenge-files.cylabacademy.net/library/9158482a92a4408128c3c320458089d0e8c2c1d8d8120ddaaabdf90397e4cedb/image.jpg).
	
Approach:
	Using exiftool on the image revealed a hidden comment which on decoding gave a private RSA key.
	This rsa key was then used to decrypt the flag using openssl's decrypt functions.

One line to rule them all:
	Always exiftool every file (image).