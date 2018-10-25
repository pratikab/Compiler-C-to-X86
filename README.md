# CS335: Compiler Design
Creating a C compiler for x86 machines in python

Requirements
------------
* Install python-2.7 and pip2 in your machine
* Install ply : ```pip install ply```
* Install pydot : ```pip install pydot```

Usage
-----
For generating parse tree on test example
* ```cd <project-top>/src```
* ```python2 cparser.py ../test/<filename> <graph_name.png>```
Graph will be generated in the test directory


For generating .S files for given .C file
* ```cd <project-top>/test```
* ```python2 ../src/code_generation.py <filename>```

Output files named a.S will be generated. Which can be further used by assembler to generate .out binary file.
* ```./run.sh```

Credits
-------

* For ANSI C Grammer [C Lex](https://www.lysator.liu.se/c/ANSI-C-grammar-l.html) [C Yacc](https://www.lysator.liu.se/c/ANSI-C-grammar-y.html) [GRAMMAR](http://www.quut.com/c/ANSI-C-grammar-l-2011.html)
* PLY python tool for Lex and Yacc [PLY](https://github.com/dabeaz/ply)
* PyDot library in python [PyDot](https://github.com/erocarrera/pydot)
* PLY Examples
* Test Examples - [merge-sort](http://quiz.geeksforgeeks.org/merge-sort/), [Quick Sort](https://www.tutorialspoint.com/data_structures_algorithms/quick_sort_program_in_c.htm), [Integer Sum](https://www.programiz.com/c-programming/examples/sum-natural-numbers). [DFS](http://www.c-program-example.com/2011/10/c-program-to-implement-depth-first.html) & [Stack](http://www.programmingsimplified.com/c/data-structures/c-stack-implementation-using-array)

Contributors
------------
* Bhangale Pratik Anil (14173)
* Shibhansh Dohare (14644)
