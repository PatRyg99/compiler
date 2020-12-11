from src.instructions import LOAD, ADD, SUB, RESET, JZERO, JUMP, DEC
from src.errors import Error
from src.blocks.constant import Constant
from src.registers import Register, RegisterManager

def operation_mapper(operation: str):
    mapper = {
        "+": Plus,
        "-": Minus,
        "*": Multiply,
        "/": Divide,
        "%": Modulo
    }
    return mapper[operation]

class BinaryOperation:
    def __init__(self, x, y, lineno):
        self.x = x
        self.y = y
        self.lineno = lineno

    def eval_num(self):
        raise NotImplementedError()

    def eval_mem(self, regx, regy):
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
        """Evaluate operation on constants"""
        return self.x.value + self.y.value

    def eval_mem(self, regx: Register, regy: Register):
        """Evaluate operation on memory registers"""
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
            JZERO(regy.name, 4),
            ADD(regz.name, regx.name),
            DEC(regy.name),
            JUMP(-3),
            RESET(regx.name),
            ADD(regx.name, regz.name),
        ]

        regz.unlock()

        return code

class Divide(BinaryOperation):
    def eval_num(self):
        if self.y.value == 0:
            return 0
        return self.x.value // self.y.value

class Modulo(BinaryOperation):
    def eval_num(self):
        if self.y.value == 0:
            return 0
        return self.x.value % self.y.value
