from solver import *

solver = Solver()
expression = input()
while expression != "":
    solution = solver.solve(expression)
    if solution is not None:
        print(solution)
    expression = input()
