#!/bin/sh
python generate_tasks.py -w world_small.txt -b data -sa -n 1000 -ps 1. -pe 0. -pe .5 -pe 1. -pi 0. -test "first order"
python generate_tasks.py -w world_large.txt -b data -sa -n 1000 -ps 1. -pe 0. -pe .5 -pe 1. -pi 0. -test "first order"
