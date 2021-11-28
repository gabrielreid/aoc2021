#!/usr/bin/env python3

import os.path
import shutil
import sys

try:
    day_num = int(sys.argv[1])
except IndexError:
    sys.stderr.write(f"Usage: {sys.argv[0]} <daynum>\n")
    sys.exit(1)

day_dir = f"day{day_num}"
if os.path.exists(day_dir):
    sys.stderr.write(f"Directory '{day_dir}' already exists")
    sys.exit(1)
os.mkdir(day_dir)
for part in ('p1', 'p2'):
    shutil.copy(os.path.join('scaffold', 'base.py'), os.path.join(day_dir, f'{part}.py'))
with open(os.path.join(day_dir, 'test_input.txt'), 'w'):
    pass
print(f"Day directory {day_dir} created")