from src.instructions import STORE, PUT, RESET, GET
from src.blocks import Constant

class Write:
    def __init__(self, x, lineno):
        self.x = x
        self.lineno = lineno

        self.regs = ["a", "b"]

    def generate_code(self):
        mem = self.regs[0]
        const = self.regs[1]

        # Writing constant
        if isinstance(self.x, Constant):
            code = self.x.generate_code(const)
            code += [RESET(mem), STORE(const, mem)]

        # Writing variable
        else:
            code = Constant(self.x.memory_block).generate_code(mem)

        # Write onto screen
        code.append(PUT(mem))

        return code

class Read:
    def __init__(self, x, lineno):
        self.x = x
        self.lineno = lineno

        self.regs = ["a"]

    def generate_code(self):
        mem = self.regs[0]
        code = Constant(self.x.memory_block).generate_code(mem)
        code.append(GET(mem))

        return code
