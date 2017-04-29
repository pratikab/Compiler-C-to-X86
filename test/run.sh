#!/bin/bash
cd ../test/
nasm -f elf32 -o a.o a.s
gcc -m32 a.o
./a.out
