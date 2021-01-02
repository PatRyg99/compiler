from src.instructions import STORE
from src.blocks.constant import Constant
from src.errors import Error


class Assignment:
    def __init__(self, var, expression, lineno):
        self.var = var
        self.expression = expression
        self.lineno = lineno

        self.regs = ["a", "b"]

    def generate_code(self):
        from src.variables import UndeclaredIterator

        # Check if var is not Iterator
        if isinstance(self.var, UndeclaredIterator):
            Error.IteratorModification.throw(self.lineno)

        # Set variable to be initilized
        self.var.initilized = True

        # Generate code for expression - to register 1
        expression_code = self.expression.generate_code(self.regs[0], self.lineno)

        # Generate code for variable memory block - to register 2
        var_code = self.var.generate_mem(self.regs[1], self.lineno)

        # Append codes and add store
        code = expression_code + var_code
        code.append(STORE(*self.regs))

        return code
