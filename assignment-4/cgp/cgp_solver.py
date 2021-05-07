from clause import *

"""
For the color grid problem, the only code you have to do is in this file.
You should replace
# your code here
by a code generating a list of clauses modeling the grid color problem
for the input file.
You should build clauses using the Clause class defined in clause.py
Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, points=None):

    expression = []

    for p in points:
        clause = Clause(size)
        p0 = int(p[0])
        p1 = int(p[1])
        p2 = int(p[2])
        #print(p)
        clause.add_positive(p0, p1, p2) # initial conditions are met
        expression.append(clause)

    for i in range(size):
        for j in range(size):
            clause = Clause(size)
            for k in range(size):
                clause.add_positive(i, j, k) # every cell has at least one color
            expression.append(clause)

    for i in range(size):
        for j in range(size):
            k1 = 0
            for k2 in range(1,size):
                clause = Clause(size)
                clause.add_negative(i, j, k1) # every cell has at most one color
                clause.add_negative(i, j, k2)
                expression.append(clause)

    for k in range(size):
        for line in range(size):
            for x1 in range(size):
                xlist = [h for h in range(size)]
                xlist.remove(x1)
                for x2 in xlist:
                    clause = Clause(size)
                    clause.add_negative(x1,line,k)
                    clause.add_negative(x2,line,k)
                    expression.append(clause)

    for k in range(size):
        for col in range(size):
            for y1 in range(size):
                ylist = [h for h in range(size)]
                ylist.remove(y1)
                for y2 in ylist:
                    clause = Clause(size)
                    clause.add_negative(col,y1,k)
                    clause.add_negative(col,y2,k)
                    expression.append(clause)

    for k in range(size):
        for i in range(size):
            for j in range(size):
                xlist = [h for h in range(size)]
                ylist = [h for h in range(size)]
                xlist.remove(i)
                ylist.remove(j)
                xdiag = []
                ydiag = []
                for a in xlist:
                    for b in ylist:
                        if a-i==b-j:
                            xdiag.append(a)
                            ydiag.append(b)

                for d in range(len(xdiag)):
                    clause = Clause(size)
                    clause.add_negative(i, j, k) # two cells on the same diagonal have different colors
                    clause.add_negative(xdiag[d], ydiag[d], k)
                    expression.append(clause)

    for k in range(size):
        for i in range(size):
            for j in range(size):
                xlist = [h for h in range(size)]
                ylist = [h for h in range(size)]
                xlist.remove(i)
                ylist.remove(j)
                xdiag = []
                ydiag = []
                for a in xlist:
                    for b in ylist:
                        if a-i==-(b-j):
                            xdiag.append(a)
                            ydiag.append(b)

                for d in range(len(xdiag)):
                    clause = Clause(size)
                    clause.add_negative(i, j, k) # two cells on the same diagonal have different colors
                    clause.add_negative(xdiag[d], ydiag[d], k)
                    expression.append(clause)


    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
