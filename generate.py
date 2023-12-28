
import random
import sys


if len(sys.argv) != 5:
    print("Usage:", sys.argv[0], " <file>")
    sys.exit(1)

w0 = float(sys.argv[2])
w1 = float(sys.argv[3])
w2 = float(sys.argv[4])

fhandle = open(sys.argv[1], 'w')
for i in range(0, 1000):
    x1 = random.uniform(0, 1000)
    x2 = random.uniform(0, 1000)
    y = 1 if w0 + w1*x1 + w2*x2 > 0 else 0
    fhandle.write(str(y) + ": " + str(x1) + " " + str(x2) + "\n")
fhandle.close()