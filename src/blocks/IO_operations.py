from src.instructions import STORE, PUT, RESET, GET
from src.blocks import Constant
from src.registers import RegisterManager


class Write:
    def __init__(self, x, lineno):
        self.x = x
        self.lineno = lineno

    def generate_code(self):
        mem = RegisterManager.get_register()
        const = RegisterManager.get_register()

        # Writing constant
        if isinstance(self.x, Constant):
            code = self.x.generate_code(const, self.lineno)
            code += [RESET(mem), STORE(const, mem)]

        # Writing variable
        else:
            code = self.x.generate_mem(mem, self.lineno)

        # Write onto screen
        code.append(PUT(mem))

        mem.unlock()
        const.unlock()

        return code


class Read:
    def __init__(self, x, lineno):
        self.x = x
        self.lineno = lineno

    def generate_code(self):
        self.x.initilized = True

        mem = RegisterManager.get_register()
        code = self.x.generate_mem(mem, self.lineno)
        code.append(GET(mem))

        mem.unlock()

        return code
