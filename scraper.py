#!/usr/bin/python3
import cv2
import numpy
import os
import sys

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], " <directory>")
    sys.exit(1)

dirname = sys.argv[1]
file_names = os.listdir(dirname)
for file_name in file_names:
    abs_name = os.path.abspath(os.path.join(dirname, file_name))
    print("Opening", file_name)
    img = cv2.imread(abs_name)
    cv2.imshow(file_name, img)
    cv2.waitKey(0)
    cv2.destroyWindow(file_name)

