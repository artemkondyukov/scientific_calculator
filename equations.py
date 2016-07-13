from postfixexpression import *


class Equations:
    @staticmethod
    def solve(left_part_string, right_part_string):
        """
        Given two infix strings does all processing related to solving an equation
        :param left_part_string:
        :param right_part_string:
        :return: err_start, err_end, err_message, interpreted_expression in case of any error
        and (varname, array representation of a polynomial, interpreted_expression otherwise)
        """
        left_part_string = left_part_string.replace(" ", "")
        right_part_string = right_part_string.replace(" ", "")

        left_side_expression = PostfixExpression(left_part_string)
        right_side_expression = PostfixExpression(right_part_string)
        left_interpreted = left_side_expression.interpreted_expression
        right_interpreted = right_side_expression.interpreted_expression
        if left_side_expression.get_error() is None:
            left_operand = left_side_expression.result
            assert left_operand is not None
        else:
            pos = left_side_expression.error_place
            return pos[0], pos[1], left_side_expression.error_msg, \
                left_interpreted + " = " + right_interpreted

        if right_side_expression.get_error() is None:
            right_operand = right_side_expression.result
            assert right_operand is not None
        else:
            shift = len(left_interpreted) + 3
            pos = right_side_expression.error_place
            pos = pos if pos != (None, None) else (-1, -1)
            return pos[0] + shift, pos[1] + shift, right_side_expression.error_msg, \
                left_interpreted + " = " + right_interpreted

        if left_side_expression.varname == right_side_expression.varname:
            if left_side_expression.varname is None:
                return None, None, "None of sides of the expression has a variable.", \
                    left_interpreted + " = " + right_interpreted
            else:
                varname = left_side_expression.varname
        else:
            if left_side_expression.varname is None:
                varname = right_side_expression.varname
            elif right_side_expression.varname is None:
                varname = left_side_expression.varname
            else:
                pos = right_interpreted.index(right_side_expression.varname)
                return pos, pos, "Several names for variable %s and %s" % \
                    (left_side_expression.varname, right_side_expression.varname), \
                    left_interpreted + " = " + right_interpreted

        return varname, (left_operand - right_operand).polynomial, \
            left_side_expression.interpreted_expression + " = " + right_side_expression.interpreted_expression
