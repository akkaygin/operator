# Operator Language
While designing my programming language, Apogee (coming soon™), I experimented with user-defined infix operators such as `x 'dot' y`, where `dot` is a user-defined procedure/operator that takes two arguments, `x` and `y`. Although I am probably not going to implement this feature in Apogee, I found the idea interesting enough to write a small interpreter based solely on that concept, but turned up to eleven—for fun and because I desperately need some toy projects to display on my GitHub profile. Right now, I am trying out Zig, but it is still outside my comfort zone, so I went with Python, as it is my primary get-stuff-done language. Everything is a floating point number or an array of floating point numbers because types are scary. Majority of the code was written in a caffeine fueled night so expect many bugs.

## Grammar
The grammar of the language is ambigious, or at least tokenizing by a formal grammar makes it harder to implement the parser, so there is no formal grammar. Source files are tokenized using a regex rule and then _vibe parsed_. I learn by observing, hopefully so do you, the `test.op` file demonstrates how to define custom operators and how to operate on arrays using three different approaches for calculating a specific number in the Fibonacci series and with a dot product operator.

## How to Try
Run `interpreter.py` with a Python 3 interpreter and specify a source file for it to execute. 
