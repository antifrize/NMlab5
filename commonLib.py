__author__ = 'Antifrize'

def floatRange(a,b,N):
    result = []
    step = (b-a)/N
    i=a
    while(i<=b):
        result.append(i)
        i+=step
    return result