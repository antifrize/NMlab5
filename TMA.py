__author__ = 'Antifrize'


import numpy.linalg
import numpy as np

def solveTMA(matrix):
    P=[]
    Q=[]
    for line  in matrix:
        a,b,c,d = line
        P.append(-c/(b+a*(P[-1] if len(P)!=0 else 0)))
        Q.append((d-a*(Q[-1] if len(Q)!=0 else 0))/(b+a*(P[-2] if len(P)>1 else 0)))
    x = []
    for i in range(len(matrix)):
        x.append(P.pop()*(x[-1] if len(x)!=0 else 0)+Q.pop())
    x.reverse()
    return x

def ssolveTMA(matrix):
    return numpy.linalg.solve([line[:-1] for line in matrix],[line[-1] for line in matrix])


def solve1(matrix):
    a = [line[0] for line in matrix]
    b = [line[1] for line in matrix]
    c = [line[2] for line in matrix]
    d = [line[3] for line in matrix]
    nf = len(a)     # number of equations
    ac, bc, cc, dc = map(np.array, (a, b, c, d))     # copy the array
    for it in xrange(1, nf):
        mc = ac[it]/bc[it-1]
        bc[it] = bc[it] - mc*cc[it-1]
        dc[it] = dc[it] - mc*dc[it-1]

    xc = ac
    xc[-1] = dc[-1]/bc[-1]

    for il in xrange(nf-2, -1, -1):
        xc[il] = (dc[il]-cc[il]*xc[il+1])/bc[il]

    del bc, cc, dc  # delete variables from memory

    return xc


# print ssolveTMA([[2,3,0,0,0,5],[1,4,-3,0,0,2],[0,-2,4,5,0,1],[0,0,2,-1,4,5],[0,0,0,-1,4,-2]])
#
# print solveTMA([[0,2,3,5],[1,4,-3,2],[-2,4,5,1],[2,-1,4,5],[-1,4,0,-2]])