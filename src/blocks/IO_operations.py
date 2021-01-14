from src.blocks import Block
from src.instructions import STORE, PUT, RESET, GET
from src.blocks import Constant
from src.registers import RegisterManager


class Write(Block):
    def __init__(self, x, lineno):
        super().__init__()

        self.x = x
        self.lineno = lineno

        self.used_regs = 0

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

        # Get number of used registers
        self.used_regs = RegisterManager.max_locked
        RegisterManager.reset_max()

        return code


class Read(Block):
    def __init__(self, x, lineno):
        super().__init__()

        self.x = x
        self.lineno = lineno

        self.used_regs = 0

    def generate_code(self):
        self.x.initilized = True

        mem = RegisterManager.get_register()
        code = self.x.generate_mem(mem, self.lineno)
        code.append(GET(mem))

        mem.unlock()

        # Get number of used registers
        self.used_regs = RegisterManager.max_locked
        RegisterManager.reset_max()

        return code
