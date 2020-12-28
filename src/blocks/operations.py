from src.instructions import LOAD, ADD, SUB, RESET, JZERO, JUMP, DEC, INC, SHL, JODD, SHR
from src.errors import Error
from src.blocks.constant import Constant

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

        self.regs = ["b", "c", "d", "e"]

    def eval_num(self):
        """Evaluate operation on constants"""
        raise NotImplementedError()

    def eval_mem(self, regx: str, regy: str):
        """Evaluate operation on memory registers"""
        raise NotImplementedError()

    def generate_code(self, regx: str):

        regy = self.regs[0]

        # If both values are numbers than evaluate constant
        if isinstance(self.x, Constant) and isinstance(self.y, Constant):
            return Constant(self.eval_num()).generate_code(regx)

        # If x is number than y is in memory
        if isinstance(self.x, Constant):
            x_code = self.x.generate_code(regx)
            y_code = Constant(self.y.memory_block).generate_code(regy)
            y_code.append(LOAD(regy, regy))

        # If y is number than x is in memory
        elif isinstance(self.y, Constant):
            y_code = self.y.generate_code(regy)
            x_code = Constant(self.x.memory_block).generate_code(regx)
            x_code.append(LOAD(regx, regx))

        # Otherwise both are in memory
        else:
            x_code = Constant(self.x.memory_block).generate_code(regx)
            x_code.append(LOAD(regx, regx))
            y_code = Constant(self.y.memory_block).generate_code(regy)
            y_code.append(LOAD(regy, regy))

        # Generating code
        code = x_code + y_code
        code += self.eval_mem(regx, regy)

        return code

class Plus(BinaryOperation):

    def eval_num(self):
        return self.x.value + self.y.value

    def eval_mem(self, regx: str, regy: str):
        return [ADD(regx, regy)]

class Minus(BinaryOperation):
    def eval_num(self):
        return min(0, self.x.value - self.y.value)

    def eval_mem(self, regx: str, regy: str):
        return [SUB(regx, regy)]

class Multiply(BinaryOperation):
    def eval_num(self):
        return self.x.value * self.y.value

    def eval_mem(self, regx: str, regy: str):
        out = self.regs[1]

        code = [
            RESET(out),

            JZERO(regx, 7),
            JODD(regx, 2),
            JUMP(2),
            ADD(out, regy),
            SHR(regx),
            SHL(regy),
            JUMP(-6),

            RESET(regx),
            ADD(regx, out)
        ]

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

    def eval_mem(self, regx: str, regy: str):

        quotient = self.regs[1]
        condition = self.regs[2]
        shifter = self.regs[3]

        code = [
            RESET(quotient),

            # Check if divisor is not 0
            JZERO(regy, 29),

            # Check if divisor bigger than divident - if so return
            RESET(condition),
            ADD(condition, regy),
            SUB(condition, regx),
            JZERO(condition, 2),
            JUMP(25),

            RESET(shifter),

            # Aligning left most bits
            RESET(condition),
            ADD(condition, regx),
            SUB(condition, regy),
            JZERO(condition, 4),
            INC(shifter),
            SHL(regy),
            JUMP(-5),

            # Move once more for equal numbers handling
            SHL(regy),
            INC(shifter),

            # Division loop
            SHR(regy),
            DEC(shifter),
            RESET(condition),
            ADD(condition, regy),
            SUB(condition, regx),
            JZERO(condition, 3),

            # If divisor is larger than divident
            SHL(quotient),
            JUMP(4),

            # Else if divident is larger or equal
            SUB(regx, regy),
            SHL(quotient),
            INC(quotient),

            # End loop when divident is back to its original form
            JZERO(shifter, 3),
            JUMP(-12),

            # If divisor is zero - reset divident
            RESET(regx)
        ]

        if not self.modulo:
            code += [RESET(regx), ADD(regx, quotient)]

        return code
