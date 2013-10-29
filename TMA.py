__author__ = 'Antifrize'

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
    return x


