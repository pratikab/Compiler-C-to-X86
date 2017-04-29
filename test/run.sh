#!/bin/bash
nasm -f elf32 -o a.o $1
gcc -m32 a.o
./a.out
