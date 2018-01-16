#!/bin/sh
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe 1. -pi 1. -pt .5
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe 1. -pi .5 -pt .5
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe 1. -pi 0. -pt .5
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe .5 -pi 1. -pt .5
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe .5 -pi .5 -pt .5
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe .5 -pi 0. -pt .5
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe 0. -pi 1. -pt .5
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe 0. -pi .5 -pt .5
python generate_tasks.py -w worlds/world_small.txt -b data -sa -n 1000 -ps 1. -pe 0. -pi 0. -pt .5

python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe 1. -pi 1. -pt .5
python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe 1. -pi .5 -pt .5
python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe 1. -pi 0. -pt .5
python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe .5 -pi 1. -pt .5
python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe .5 -pi .5 -pt .5
python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe .5 -pi 0. -pt .5
python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe 0. -pi 1. -pt .5
python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe 0. -pi .5 -pt .5
python generate_tasks.py -w worlds/world_large.txt -b data -sa -n 1000 -ps 1. -pe 0. -pi 0. -pt .5
