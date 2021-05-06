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
    #print(size, points)

    for p in points:
        clause = Clause(size)
        p0 = int(p[0])
        p1 = int(p[1])
        p2 = int(p[2])
        #print(p0,p1,p2)
        clause.add_positive(p0, p1, p2) # initial conditions are met
        expression.append(clause)

    for i in range(size):
        for j in range(size):
            clause = Clause(size)
            for k in range(size):
                clause.add_positive(i, j, k) # every cell has at least one color
            expression.append(clause)

            for k in range(size): 
                xlist = [h for h in range(size)]
                xlist.remove(i)
                ylist = [h for h in range(size)]
                ylist.remove(j)
                xdiag = []
                ydiag = []
                for a in xlist:
                    for b in ylist:
                        if abs(a-i)==abs(b-j):
                            xdiag.append(a)
                            ydiag.append(b)

                for x in xlist:
                    clause = Clause(size)
                    clause.add_negative(i, j, k) # two cells on the same line have different colors
                    clause.add_negative(x, j, k) 
                    expression.append(clause)

                for y in ylist:
                    clause = Clause(size)
                    clause.add_negative(i, j, k) # two cells in the same column have different colors
                    clause.add_negative(i, y, k) 
                    expression.append(clause)

                for d in range(len(xdiag)):
                    clause = Clause(size)
                    clause.add_negative(i, j, k) # two cells on the same diagonal have different colors
                    clause.add_negative(xdiag[d], ydiag[d], k) 
                    expression.append(clause)

            for k1 in range(size):
                for k2 in range(size):
                    clause = Clause(size)
                    clause.add_negative(i, j, k1) # every cell has at most one color
                    clause.add_negative(i, j, k2)
                    expression.append(clause)
                
    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
