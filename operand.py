import math


class Operand:
    # We represent operands as polynomials.
    # It is possible until we have to work with several variables.
    def __init__(self, polynomial):
        self.polynomial = []
        self.polynomial.extend(list(polynomial))

    def __add__(self, other):
        if len(self.polynomial) < len(other.polynomial):
            tmp_self = self.polynomial + [0] * (len(other.polynomial) - len(self.polynomial))
            return Operand(list(map(lambda t: t[0] + t[1], zip(tmp_self, other.polynomial))))
        else:
            tmp_other = other.polynomial + [0] * (len(self.polynomial) - len(other.polynomial))
            return Operand(list(map(lambda t: t[0] + t[1], zip(self.polynomial, tmp_other))))

    def __sub__(self, other):
        if len(self.polynomial) < len(other.polynomial):
            tmp_self = self.polynomial + [0] * (len(other.polynomial) - len(self.polynomial))
            return Operand(list(map(lambda t: t[0] - t[1], zip(tmp_self, other.polynomial))))
        else:
            tmp_other = other.polynomial + [0] * (len(self.polynomial) - len(other.polynomial))
            return Operand(list(map(lambda t: t[0] - t[1], zip(self.polynomial, tmp_other))))

    def __mul__(self, other):
        result = [0] * (len(self.polynomial) + len(other.polynomial) - 1)
        for i, term in enumerate(self.polynomial):
            tmp_poly = [0] * i + \
                       [t * term for t in other.polynomial] + \
                       [0] * (len(result) - len(other.polynomial))

            result = [r + t for r, t in zip(result, tmp_poly)]
        return Operand(result)

    def __truediv__(self, other):
        if len(other.polynomial) > len(self.polynomial):
            raise NotImplementedError("Negative degrees aren't implemented yet")

        dividend = Operand(self.polynomial)
        result = []
        while len(dividend.polynomial) >= len(other.polynomial):
            coef = dividend.polynomial[-1] / other.polynomial[-1]
            result += [coef]
            dividend -= Operand([coef]) * other * Operand([0] *
                                                          (len(dividend.polynomial) - len(other.polynomial)) + [1])
            dividend.polynomial.pop()
        return Operand(result[::-1])

    def __eq__(self, other):
        if len(self.polynomial) != len(other.polynomial):
            return False
        for term_s, term_o in zip(self.polynomial, other.polynomial):
            if term_s != term_o:
                return False
        return True

    def log(self, base):
        if len(self.polynomial) > 1:
            raise NotImplementedError("Logarithms are supported only for plain numbers")

        if isinstance(base, Operand):
            if len(base.polynomial) > 1:
                raise NotImplementedError("Logarithms are supported only for plain numbers")
            return Operand([math.log(self.polynomial[0], base.polynomial[0])])
        elif isinstance(base, float):
            return Operand([math.log(self.polynomial[0], base)])
        else:
            raise ValueError("Unacceptable base for logarithm")

    def varstring(self, varname):
        result = ""
        if self.polynomial[0] != 0:
            coef = self.polynomial[0]
            coef = math.floor(coef) if coef == math.floor(coef) else coef
            coef = str(coef) if coef != 1 else ""
            result += coef
        if len(self.polynomial) > 1:
            if result:
                result += "+"
            coef = self.polynomial[1]
            coef = math.floor(coef) if coef == math.floor(coef) else coef
            coef = str(coef) if coef != 1 else ""
            result += coef + varname
        return result
