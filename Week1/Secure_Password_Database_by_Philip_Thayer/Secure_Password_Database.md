# Secure_Password_Database
## Approach
* Decompiled the vuln binary
* These bytes are being stored, must be for a reason![[Screenshot 2026-09-27 at 3.28.27 AM.png]]
* Found where it is being used. it is being xor'ed with 0xAA![[Screenshot 2026-09-27 at 3.27.38 AM.png]]
* a1 is being appended with a 0 aswell could be a string terminator
* Found the hashing function which claude tells is djb2 hash![[Screenshot 2026-09-27 at 2.51.58 AM.png]]
  
  
## Solution
* Run a script written by claude which does the following conversion 
```
stored integers -> unsigned 8byte integers -> xor with 0xAA 
```
* hash the output with djb2
* input hash as login credentials
* no feedback so assumed to be incorrect
* convert to ascii because every value gives a valid character so high possibility it may work
* This hash is again inputted as login credentials
* the flag is then printed.
## Flag

```
academy{n0_r4t3_n0_4uth_b8c7ed63}
``` 

## Takeaway
Always check how much data is just being stored/hardcoded + try conversion to ascii when the value ends with a 0 whenever possible