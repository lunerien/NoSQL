#!/bin/bash
for I in {0..15}
do
  ../bin/python3 lab2create.py ${I}
  time ../bin/python3 lab2test.py
done