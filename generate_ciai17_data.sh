#!/bin/sh
python generate_tasks.py -w world_small.txt -b data -sa -n 1000 -ps 1. -pe .5 -pi .5 -test "first order" -test "second order" -test "reality" -test "memory"
python generate_tasks.py -w world_large.txt -b data -sa -n 1000 -ps 1. -pe .5 -pi .5 -test "first order" -test "second order" -test "reality" -test "memory"
