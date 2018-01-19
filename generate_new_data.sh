#!/bin/sh
python generate_tasks.py -w world_small.txt -w world_large.txt -b data -sa -n 1000 -ps 1. -pe .666 -pi .5 -test "first order" -test "second order" -test "reality" -test "memory"
