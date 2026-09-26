Description:
	Proper session timeout controls are critical for securing user accounts. If a user logs in on a public or shared computer but doesn’t explicitly log out (instead simply closing the browser tab), and session expiration dates are misconfigured, the session may remain active indefinitely.
	  This then allows an attacker using the same browser later to access the user’s account without needing credentials, exploiting the fact that sessions never expire and remain authenticated.
	  Your friend tells you to check out a new social media platform he built a few years ago. Although its still under development, he said the site is almost complete. He also mentioned that he hates constantly logging into sites, and so has made his page that 'once you login, you never have to log-out again'!
	  Browse here, and find the flag! 
  
Approach: 
	First registered a new account on the website, then noticed the comment which told to check /sessions
	/sessions gave me the admin's login cookie data value which i then used to replace my own session data to admins cookie session data and reloaded the page.
	The flag was revealed.

One line to remember them all:
	Always check /sessions and cookies + always register.