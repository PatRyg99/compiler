from src.instructions import STORE
from src.blocks.constant import Constant

class Assignment:
    def __init__(self, var, expression, lineno):
        self.var = var
        self.expression = expression
        self.lineno = lineno

    def generate_code(self):
        code = []

        reg_1 = "a"
        reg_2 = "b"

        expression_code = self.expression.generate_code(reg=reg_1)
        var_code = Constant(self.var.memory_block).generate_code(reg=reg_2)

        code += expression_code + var_code
        code.append(STORE(reg_1, reg_2))

        return code
