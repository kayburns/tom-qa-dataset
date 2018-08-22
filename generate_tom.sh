#!/bin/sh
python create_world.py
python generate_tasks.py -w world_large.txt -b data -n 1000 -ptn=0 -test='memory' # -test args is dummy
python generate_tasks.py -easy -w world_large.txt -b data -n 1000 -ptn=0 -test='memory' # -test args is dummy
python generate_tasks.py -w world_large.txt -b data -n 1000 -ptn=.1 -test='memory' # -test args is dummy
python generate_tasks.py -easy -w world_large.txt -b data -n 1000 -ptn=.1 -test='memory' # -test args is dummy
