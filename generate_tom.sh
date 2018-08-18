#!/bin/sh
python create_world.py
for i in {0,.1}
do
    python generate_tasks.py -w world_large.txt -b data -n 1000 -ptn=${i} -test='memory' # -test args is dummy
    python generate_tasks.py -easy -w world_large.txt -b data -n 1000 -ptn=${i} -test='memory' # -test args is dummy
done
