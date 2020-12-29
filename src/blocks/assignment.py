from src.instructions import STORE
from src.blocks.constant import Constant


class Assignment:
    def __init__(self, var, expression, lineno):
        self.var = var
        self.expression = expression
        self.lineno = lineno

        self.regs = ["a", "b"]

    def generate_code(self):

        # Generate code for expression - to register 1
        expression_code = self.expression.generate_code(self.regs[0])

        # Generate code for variable memory block - to register 2
        var_code = self.var.generate_mem(self.regs[1])

        # Append codes and add store
        code = expression_code + var_code
        code.append(STORE(*self.regs))

        return code
