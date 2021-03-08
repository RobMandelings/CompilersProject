#!/bin/bash

java -jar /usr/local/lib/antlr-4.9.1-complete.jar -o src/antlr4_gen/ -Dlanguage=Python3 C.g4 -visitor
