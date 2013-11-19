__author__ = 'Antifrize'


import numpy.linalg

def solveTMA(matrix):
    P=[]
    Q=[]
    for line  in matrix:
        a,b,c,d = line
        P.append(c/(b-a*(P[-1] if len(P)!=0 else 0)))
        Q.append((a*(Q[-1] if len(Q)!=0 else 0)-d)/(b-a*(P[-2] if len(P)>1 else 0)))
    x = []
    for i in range(len(matrix)):
        x.append(P.pop()*(x[-1] if len(x)!=0 else 0)+Q.pop())
    return x

def ssolveTMA(matrix):
    return numpy.linalg.solve([line[:-1] for line in matrix],[line[-1] for line in matrix])



# print ssolveTMA([[2,3,0,0,0,5],[1,4,-3,0,0,2],[0,-2,4,5,0,1],[0,0,2,-1,4,5],[0,0,0,-1,4,-2]])
#
# print solveTMA([[0,2,3,5],[1,4,-3,2],[-2,4,5,1],[2,-1,4,5],[-1,4,0,-2]])