from src.instructions import *
from src.blocks import Constant

class Write:
    def __init__(self, x, lineno):
        self.x = x
        self.lineno = lineno

    def generate_code(self, reg: str = "a"):

        # Writing constant
        if type(self.x) == int:
            const_code = Constant(x).generate_code(reg)
            code += const_code
            code.append(STORE(reg, reg))
        
        # Writing variable
        else:
            code = Constant(self.x.memory_block).generate_code(reg)

        code.append(PUT(reg))
        return code