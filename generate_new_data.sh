#!/bin/sh
python generate_tasks.py -w world_large.txt -b data -n 10 -ps 1. -pe .666 -pi .5 -test "first order" -test "second order" -test "reality" -test "memory"
