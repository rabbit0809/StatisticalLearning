import numpy
import os
import sys
class parser:
    def __init__(self, abs_name) -> None:
        fhandle = open(abs_name, 'r')
        if not fhandle:
            raise Exception("Could not open file", abs_name)
        
        self.numvars = None
        self.feat_vecs = []
        for line in fhandle.readlines():
            y, x = line.split(':')
            x = x.split()
            line_numvars = len(x)
            y = float(y)
            if self.numvars is None:
                self.numvars = line_numvars
            elif self.numvars != line_numvars:
                raise Exception("Inconsistent number of variables in", abs_name)
            print(x)
            x = [ float(i) for i in x ]
            x = numpy.array(x)
            self.feat_vecs.append((y, x))
        fhandle.close()
        self.weights = numpy.zeros(self.numvars)

    def train(self, num_epochs, eta) -> None:
        for epoch in range(0, num_epochs):
            dLdm = numpy.zeros(self.numvars)
            for y, x in self.feat_vecs:
                dLdm += (y - numpy.dot(self.weights, x)) * x
            norm = numpy.sqrt(numpy.dot(dLdm, dLdm))
            uvect = dLdm / norm
            print("dLdm", eta * dLdm/len(self.feat_vecs), "unit vector", uvect)
            self.weights += eta * uvect
            print("weights", self.weights)

    def predict(self, x) -> float:
        return numpy.dot(self.weights, x)

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], " <file>")
    sys.exit(1)

abs_name = sys.argv[1]
my_parser = parser(abs_name)
my_parser.train(100, 0.1)
print(my_parser.weights)
print(my_parser.predict(numpy.array([99, 4, 2, 3])))