## Approach
* First looked at the users.db database which showed that the admin login had 2FA enabled and the hashes of every user were listed aswell.
* The password hashes looked very much like sha256 hashes so putting the hashes into crackstation revealed the actual passwords.
* Logging in with any other account other than the admin gives a clear deadend with "no flag for you" printed on the site.
* Logging in with admin creds asks for a 4 digit otp 
* Since it is only a 4 digit otp and no clear signs of a time limit on the otp, tried bruteforcing it.
* it had a request rate limit after which it just disconnected any new connection; bruteforce is still possible but would require like 1 hour to complete
* Looked at app.py which showed its a flask application
* observed that app.py stores the otp locally as a cookie
* find out that flask cookies are easily decodable using flask-unsign --decode
## Solution
* export the sql database to an excel file for ease of view
* decode admins password hash using crackstation
* decode the session cookie and obtained the otp using flask-unsign
* this gave me access to the admin account
* the flag was printed in the very next page

## Flag
academy{sa3S_sEc9t_65bbf411}

## Takeaway
Flask apps have easy cookie data
