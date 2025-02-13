# import OS module
import os
 
# This is my path
path = "./crop_part1"
 
# to store files in a list
list = []
 
# dirs=directories
for (root, dirs, file) in os.walk(path):
    for f in file:
        list.append(f)

with open(r'./names.txt', 'w') as fp:
    for item in list:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')