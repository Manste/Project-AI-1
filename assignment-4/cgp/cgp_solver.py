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

    limit = sum(list(range(size)))

    for i in range(size): # rows
        for j in range(size): # columns
            clause_self = Clause(size)
            clause_neighbors = Clause(size)
            clause_horinzontal = Clause(size)
            clause_vertical = Clause(size)
            clause_diagonal = Clause(size)
            for k in range(size): # colors
                clause_self.add_positive(i, j, k)
                for c in range(size):


    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
