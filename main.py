from solver import *

solver = Solver()
expression = input()
while expression != "":
    solution = solver.evaluate_infix(expression)
    if solution is not None:
        print(solution)
    expression = input()
