from src.instructions import STORE, PUT, RESET
from src.blocks import Constant
from src.registers import Register, RegisterManager

class Write:
    def __init__(self, x, lineno):
        self.x = x
        self.lineno = lineno

    def generate_code(self):

        # Get free register
        regx = RegisterManager.get_free_register()
        regy = RegisterManager.get_free_register()

        # Writing constant
        if isinstance(self.x, Constant):
            code = self.x.generate_code(regy.name)
            code += [RESET(regx.name), STORE(regy.name, regx.name)]

        # Writing variable
        else:
            code = Constant(self.x.memory_block).generate_code(regx)

        # Write onto screen
        code.append(PUT(regx.name))

        # Unlock register
        regx.unlock()
        regy.unlock()

        return code
