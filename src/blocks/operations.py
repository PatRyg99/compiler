from src.instructions import LOAD, ADD, SUB, RESET, JZERO, JUMP, DEC, INC, SHL, JODD, SHR
from src.errors import Error
from src.blocks.constant import Constant
from src.registers import Register, RegisterManager

def operation_mapper(operation: str):
    mapper = {
        "+": Plus,
        "-": Minus,
        "*": Multiply,
        "/": Divide,
        "%": lambda x, y, lineno: Divide(x, y, lineno, modulo=True)
    }
    return mapper[operation]

class BinaryOperation:
    def __init__(self, x, y, lineno):
        self.x = x
        self.y = y
        self.lineno = lineno

    def eval_num(self):
        """Evaluate operation on constants"""
        raise NotImplementedError()

    def eval_mem(self, regx, regy):
        """Evaluate operation on memory registers"""
        raise NotImplementedError()

    def generate_code(self, regx: Register):

        # If both values are numbers than evaluate constant
        if isinstance(self.x, Constant) and isinstance(self.y, Constant):
            return Constant(self.eval_num()).generate_code(regx)

        regy = RegisterManager.get_free_register()

        # If x is number than y is in memory
        if isinstance(self.x, Constant):
            x_code = self.x.generate_code(regx)
            y_code = Constant(self.y.memory_block).generate_code(regy)
            y_code.append(LOAD(regy.name, regy.name))

        # If y is number than x is in memory
        elif isinstance(self.y, Constant):
            y_code = self.y.generate_code(regy)
            x_code = Constant(self.x.memory_block).generate_code(regx)
            x_code.append(LOAD(regx.name, regx.name))

        # Otherwise both are in memory
        else:
            x_code = Constant(self.x.memory_block).generate_code(regx)
            x_code.append(LOAD(regx.name, regx.name))
            y_code = Constant(self.y.memory_block).generate_code(regy)
            y_code.append(LOAD(regy.name, regy.name))

        # Generating code
        code = x_code + y_code
        code += self.eval_mem(regx, regy)

        regy.unlock()

        return code

class Plus(BinaryOperation):

    def eval_num(self):
        return self.x.value + self.y.value

    def eval_mem(self, regx: Register, regy: Register):
        return [ADD(regx.name, regy.name)]

class Minus(BinaryOperation):
    def eval_num(self):
        return min(0, self.x.value - self.y.value)

    def eval_mem(self, regx: Register, regy: Register):
        return [SUB(regx.name, regy.name)]

class Multiply(BinaryOperation):
    def eval_num(self):
        return self.x.value * self.y.value

    def eval_mem(self, regx: Register, regy: Register):
        regz = RegisterManager.get_free_register()

        code = [
            RESET(regz.name),

            JZERO(regx.name, 7),
            JODD(regx.name, 2),
            JUMP(2),
            ADD(regz.name, regy.name),
            SHR(regx.name),
            SHL(regy.name),
            JUMP(-6),

            RESET(regx.name),
            ADD(regx.name, regz.name)
        ]

        regz.unlock()

        return code

class Divide(BinaryOperation):

    def __init__(self, x: int, y: int, lineno: int, modulo: bool = False):
        super().__init__(x, y, lineno)
        self.modulo = modulo

    def eval_num(self):
        if self.y.value == 0:
            return 0

        if self.modulo:
            return self.x.value % self.y.value
        else:
            return self.x.value // self.y.value

    def eval_mem(self, regx: Register, regy: Register):
        regz = RegisterManager.get_free_register()
        regw = RegisterManager.get_free_register()
        regv = RegisterManager.get_free_register()

        code = [
            RESET(regz.name),

            # Check if divisor is not 0
            JZERO(regy.name, 22),

            RESET(regv.name),

            # Aligning left most bits
            RESET(regw.name),
            ADD(regw.name, regx.name),
            SUB(regw.name, regy.name),
            JZERO(regw.name, 4),
            INC(regv.name),
            SHL(regy.name),
            JUMP(-5),

            # Division loop
            SHR(regy.name),
            DEC(regv.name),
            RESET(regw.name),
            ADD(regw.name, regy.name),
            SUB(regw.name, regx.name),
            JZERO(regw.name, 3),

            # If divisor is larger than divident
            SHL(regz.name),
            JUMP(4),

            # Else if divident is larger or equal
            SUB(regx.name, regy.name),
            SHL(regz.name),
            INC(regz.name),

            # End loop when divident is back to its original form
            JZERO(regv.name, 3),
            JUMP(-12),

            # If divident is zero
            RESET(regx.name)
        ]

        if not self.modulo:
            code += [RESET(regx.name), ADD(regx.name, regz.name)]

        regz.unlock()
        regw.unlock()
        regv.unlock()

        return code
