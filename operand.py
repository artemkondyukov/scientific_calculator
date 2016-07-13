import math


class Operand:
    # We represent operands as polynomials.
    # It is possible until we have to work with several variables.
    def __init__(self, polynomial):
        self.polynomial = []
        self.polynomial.extend(list(polynomial))
        while len(self.polynomial) > 1:
            if self.polynomial[-1] == 0:
                self.polynomial.pop()
            else:
                break

    def __add__(self, other):
        if len(self.polynomial) < len(other.polynomial):
            tmp_self = self.polynomial + [0] * (len(other.polynomial) - len(self.polynomial))
            result = list(map(lambda t: t[0] + t[1], zip(tmp_self, other.polynomial)))
            while len(result) > 1 and result[-1] == 0:
                result.pop()
            return Operand(result)
        else:
            tmp_other = other.polynomial + [0] * (len(self.polynomial) - len(other.polynomial))
            result = list(map(lambda t: t[0] + t[1], zip(self.polynomial, tmp_other)))
            while len(result) > 1 and result[-1] == 0:
                result.pop()
            return Operand(result)

    def __sub__(self, other):
        if len(self.polynomial) < len(other.polynomial):
            tmp_self = self.polynomial + [0] * (len(other.polynomial) - len(self.polynomial))
            result = list(map(lambda t: t[0] - t[1], zip(tmp_self, other.polynomial)))
            while len(result) > 1 and result[-1] == 0:
                result.pop()
            return Operand(result)
        else:
            tmp_other = other.polynomial + [0] * (len(self.polynomial) - len(other.polynomial))
            result = list(map(lambda t: t[0] - t[1], zip(self.polynomial, tmp_other)))
            while len(result) > 1 and result[-1] == 0:
                result.pop()
            return Operand(result)

    def __mul__(self, other):
        result = [0] * (len(self.polynomial) + len(other.polynomial) - 1)
        for i, term in enumerate(self.polynomial):
            tmp_poly = [0] * i + \
                       [t * term for t in other.polynomial] + \
                       [0] * (len(result) - len(other.polynomial))

            result = [r + t for r, t in zip(result, tmp_poly)]
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        return Operand(result)

    def __truediv__(self, other):
        if len(other.polynomial) > len(self.polynomial):
            raise NotImplementedError("Error: negative degrees aren't implemented yet.")

        dividend = Operand(self.polynomial)
        result = []
        while len(dividend.polynomial) > len(other.polynomial):
            try:
                coef = dividend.polynomial[-1] / other.polynomial[-1]
            except ZeroDivisionError:
                raise ZeroDivisionError("Error: division by zero.")
            result += [coef]
            div_len = len(dividend.polynomial)
            dividend -= Operand([coef]) * other * Operand([0] *
                                                          (len(dividend.polynomial) - len(other.polynomial)) + [1])

            # After subtraction the degree of dividend MUST decrease
            if div_len - len(dividend.polynomial) == 0:
                dividend.polynomial.pop()

        try:
            coef = dividend.polynomial[-1] / other.polynomial[-1]
        except ZeroDivisionError:
            raise ZeroDivisionError("Error: division by zero.")
        result += [coef]

        result = result[::-1]
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        return Operand(result)

    def __eq__(self, other):
        if len(self.polynomial) != len(other.polynomial):
            return False
        for term_s, term_o in zip(self.polynomial, other.polynomial):
            if term_s != term_o:
                return False
        return True

    def log(self, base):
        if len(self.polynomial) > 1:
            raise NotImplementedError("Error: logarithms are supported only for plain numbers.")

        if isinstance(base, Operand):
            if len(base.polynomial) > 1:
                raise NotImplementedError("Error: logarithms are supported only for plain numbers.")
            if base.polynomial[0] <= 0 or base.polynomial[0] == 1:
                raise ValueError("Error: illegal base for logarithm.")
            if self.polynomial[0] <= 0:
                raise ValueError("Error: illegal value for logarithm.")
            return Operand([math.log(self.polynomial[0], base.polynomial[0])])
        elif isinstance(base, float):
            if base <= 0 or base == 1:
                raise ValueError("Error: illegal base for logarithm.")
            if self.polynomial[0] <= 0:
                raise ValueError("Error: illegal value for logarithm.")
            return Operand([math.log(self.polynomial[0], base)])
        else:
            raise ValueError("Error: unacceptable base for logarithm.")

    def __str__(self):
        return str(self.polynomial)

    def __repr__(self):
        return str(self.polynomial)

    def varstring(self, varname):
        result = ""
        if self.polynomial[0] != 0:
            coefficient = self.polynomial[0]
            coefficient = math.floor(coefficient) if coefficient == math.floor(coefficient) else coefficient
            result += str(coefficient)
        if len(self.polynomial) == 2:
            if result != "":
                result += " + "
            coefficient = self.polynomial[1]
            coefficient = math.floor(coefficient) if coefficient == math.floor(coefficient) else coefficient
            coefficient = str(coefficient) if coefficient != 1 else ""
            result += coefficient + varname
        elif len(self.polynomial) > 2:
            raise NotImplementedError("Error: degrees higher than 1 aren't implemented yet.")
        return result
