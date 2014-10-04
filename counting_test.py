import random
import math
import time
import numpy

if __name__ == '__main__':
    arr = []
    temp = [10, 50, 100, 200, 400]
    for i in range(1000):
        arr.append(math.ceil(random.random()*temp[i % 5]))

    t = time.time()
    dict((i, arr.count(i)) for i in arr)
    print "Dict count %f\n" % (time.time() - t)

    t = time.time()
    dict((i, arr.count(i)) for i in set(arr))
    print "Set & count %f\n" % (time.time() - t)

    t = time.time()
    set_arr = set(arr)
    dict((i, arr.count(i)) for i in set_arr)
    print "Initialized set & count %f\n" % (time.time() - t)

    t = time.time()
    numpy.bincount(arr)
    print "Numpy %f\n" % (time.time() - t)
    


