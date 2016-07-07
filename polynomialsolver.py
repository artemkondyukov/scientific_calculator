class PolynomialSolver:
    @staticmethod
    def solve(polynomial):
        """
        Numerically solves a polynomial
        :param polynomial: array of coefficients
        :return: an array of solutions
        solution is an array of two elements where the second value is
        either 1 (in this case the first element represents a possible value of variable)
        or 0 (in this case a solution is actually a simplification and all occurrences of variable were cancelled)
        """
        if len(polynomial) == 1:
            return [polynomial[0] + [0]]
        elif len(polynomial) == 2:
            num_result = -polynomial[0] / polynomial[1]
            return [num_result + [1]]
        else:
            raise NotImplementedError("Only linear equations are supported by now!")
