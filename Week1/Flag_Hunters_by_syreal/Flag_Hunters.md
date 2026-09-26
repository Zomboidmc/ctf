Description:
	Lyrics jump from verses to the refrain kind of like a subroutine call. There's a hidden refrain this program doesn't print by default. Can you get it to print it? There might be something in it for you.

 Approach
* Looked at the python file
* obversed that the line processor in the source processes the lyrics based on string matching
* this string matching included strings inputted by the user in the "crowd: " part
* ";" splits the line into two allowing for execution of any special string.
* inputting ";RETURN 0" in the crowd section since return n repeats the nth verse again
* this gives the flag in plain text printed as one of the lyrics lines.

One line to remember them all:
	Always check for unchecked user inputs
