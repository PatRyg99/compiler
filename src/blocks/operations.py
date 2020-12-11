from src.instructions import *
from src.errors import division_by_zero_error
from src.blocks.constant import Constant

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

    def generate_code(self, reg: str = "a"):
        
        # If both values are numbers than evaluate constant
        if type(self.x) == int and type(self.y) == int:
            return Constant(self.eval()).generate_code(reg=reg)

        # If x is number than compute it as constant
        if type(self.x) == int:
            x_code = Constant(self.x).generate_code(reg)
        else:
            x_code = Constant(self.x.memory_block).generate_code(reg)
            x_code.append(LOAD(reg, reg))
        
        # If y is number than compute is as constant
        if type(self.y) == int:
            y_code = Constant(self.y).generate_code(reg="c")
        else:
            y_code = Constant(self.y.memory_block).generate_code(reg="c")
            y_code.append(LOAD("c", "c"))

        code = x_code + y_code
        return code + self.eval_mem(reg_1=reg, reg_2="c", reg_3="d")

class Plus(BinaryOperation):

    def eval(self):
        """Evaluate operation on constants"""
        return self.x + self.y

    def eval_mem(self, reg_1: str, reg_2: str, reg_3: str):
        """Evaluate operation on memory registers"""
        return [ADD(reg_1, reg_2)]

class Minus(BinaryOperation):
    def eval(self):
        return min(0, self.x - self.y)

    def eval_mem(self, reg_1: str, reg_2: str, reg_3: str):
        return [SUB(reg_1, reg_2)]
    
class Multiply(BinaryOperation):
    def eval(self):
        return self.x * self.y

    def eval_mem(self, reg_1: str, reg_2: str, reg_3: str):
        code = [
            RESET(reg_3),
            JZERO(reg_2, 4),
            ADD(reg_3, reg_1),
            DEC(reg_2),
            JUMP(-3),
            RESET(reg_1),
            ADD(reg_1, reg_3)
        ]

        return code
        

class Divide(BinaryOperation):
    def eval(self):
        if self.y == 0:
            division_by_zero_error(self.lineno)
        return self.x // self.y

class Modulo(BinaryOperation):
    def eval(self):
        if self.y == 0:
            division_by_zero_error(self.lineno)
        return self.x % self.y
        