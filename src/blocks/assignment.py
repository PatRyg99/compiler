from src.instructions import STORE
from src.blocks.constant import Constant
from src.errors import Error
from src.registers import RegisterManager
from src.blocks import Block


class Assignment(Block):
    def __init__(self, var, expression, lineno):
        super().__init__()

        self.var = var
        self.expression = expression
        self.lineno = lineno

    def generate_code(self):
        from src.variables import UndeclaredIterator

        # Check if var is not Iterator
        if isinstance(self.var, UndeclaredIterator):
            Error.IteratorModification.throw(self.lineno)

        # Set variable to be initilized
        self.var.initilized = True

        # Generate code for expression - to register 1
        expr_reg = RegisterManager.get_register()
        expression_code = self.expression.generate_code(expr_reg, self.lineno)

        # Generate code for variable memory block - to register 2
        var_reg = RegisterManager.get_register()
        var_code = self.var.generate_mem(var_reg, self.lineno)

        # Append codes and add store
        code = expression_code + var_code
        code.append(STORE(expr_reg, var_reg))

        # Unlock registers
        expr_reg.unlock()
        var_reg.unlock()

        return code
