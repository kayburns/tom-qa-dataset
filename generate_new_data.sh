#!/bin/sh
python generate_tasks.py -w world_large.txt -b data -n 1000 -ps 1. -pe .666 -pi .5 -ptn=.10 -test='memory' # -test args is dummy
