from src.instructions import STORE, PUT
from src.blocks import Constant
from src.registers import Register, RegisterManager

class Write:
    def __init__(self, x, lineno):
        self.x = x
        self.lineno = lineno

    def generate_code(self):

        # Get free register
        reg = RegisterManager.get_free_register()

        # Writing constant
        if isinstance(self.x, Constant):
            code = self.x.generate_code(reg.name)
            code.append(STORE(reg.name, reg.name))

        # Writing variable
        else:
            code = Constant(self.x.memory_block).generate_code(reg)

        # Write onto screen
        code.append(PUT(reg.name))

        # Unlock register
        reg.unlock()

        return code
