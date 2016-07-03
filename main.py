from solver import *

solver = Solver()
expression = input()
print(solver.solve(expression))
while expression != "":
    expression = input()
    print(solver.solve(expression))
