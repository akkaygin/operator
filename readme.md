# Operator Language Interpreter
While designing my programming language, Apogee (coming soon™), I experimented with user-defined operators such as `x 'dot' y`, where dot is a user-defined procedure/operator that takes two arguments, `x` and `y`. Although I am probably not going to implement this feature in Apogee, I found the idea interesting enough to write a small interpreter based solely on that concept—for fun and because I desperately need some toy projects to display on my GitHub profile. Right now, I am trying out Zig, but it is still outside my comfort zone, so I went with Python, as it is my primary get-stuff-done language. In the background every line is tokenized, parsed and executed. Everything is a floating point number. I got bored so I did not add proper conditionals or loops, the language is still Turing complete so I am fine with leaving it as is. Expect many bugs. Also i do not support 'structs' so the `'dot'` example is not possible (as a vector dot operator).

## Running
Run `interpreter.py` with a Python 3 interpreter and specify a source file for it to execute.

### Grammar
The grammar of the language is ambigious, or at least tokenizing by a formal grammar makes it harder to implement the parser, so there is no formal grammar but an dumb regex rule
`\s*(?:('\w\S*')|(\w\S*')|('\w\S*)|(\d+)|(\w+)|(.+))`.

### Demo
```
cat <<EOF > fibonacci.op
operator right CUSTOM fibonacci' count
  0 'returnif' count 'eq' 0;
  1 'returnif' count 'lt' 3;
  return' ((fibonacci' (count 'sub' 1)) 'add' (fibonacci' (count 'sub' 2)));
end

fibonacci' 
EOF
```
```
> interpreter.py fibonacci.op
5
```