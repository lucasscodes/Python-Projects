import time
import numpy

#Default is 19 digits after dot
def pythonDiv(a,b):
    return a/b
def numpyDiv(a,b):
    return numpy.divide(a,b)
def myDiv(a,b):
    return 0
    #TODO: Bitwise inside python

def times():
    functions = [pythonDiv,numpyDiv,myDiv]
    times = []
    repetitions = 1000
    for func in functions:
        i = repetitions
        mem = []
        while i > 0:
            start = time.perf_counter_ns()
            func(1,137)
            end = time.perf_counter_ns()
            mem += [end - start]
            i -= 1
        avg = sum(mem)/repetitions
        times += [(func.__name__, avg)]
    return times

for data in times():
    print(data[0], "brauchte im Schnitt:", data[1], "ns!" )