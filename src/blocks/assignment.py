from src.instructions import STORE
from src.blocks.constant import Constant
from src.registers import RegisterManager

class Assignment:
    def __init__(self, var, expression, lineno):
        self.var = var
        self.expression = expression
        self.lineno = lineno

    def generate_code(self):

        # Get unused registers
        reg_1 = RegisterManager.get_free_register()
        reg_2 = RegisterManager.get_free_register()

        # Generate code for expression - to register 1
        expression_code = self.expression.generate_code(reg_1)

        # Generate code for variable memory block - to register 2
        var_code = Constant(self.var.memory_block).generate_code(reg_2)

        # Append codes and add store
        code = expression_code + var_code
        code.append(STORE(reg_1.name, reg_2.name))

        # Unlock registers after use
        reg_1.unlock()
        reg_2.unlock()

        return code
