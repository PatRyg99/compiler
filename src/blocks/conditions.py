from src.errors import Error
from src.blocks.constant import Constant
from src.instructions import LOAD, ADD, SUB, RESET, JZERO, JUMP, DEC, INC, SHL, JODD, SHR

def condition_mapper(operation: str):
    mapper = {
        "=": Equals,
        "!=": NotEquals,
        "<": Lesser,
        ">": Greater,
        "<=": LEQ,
        ">=": GEQ
    }
    return mapper[operation]

class Condition:
    def __init__(self, x, y, lineno):
        self.x = x
        self.y = y
        self.lineno = lineno

        self.regs = ["a", "b"]

    def eval_num(self):
        """Evaluate condition on constants"""
        raise NotImplementedError()

    def eval_mem(self, regx: str, regy: str):
        """Evaluate condition on memory registers"""
        raise NotImplementedError()

    def generate_code(self, regc: str):

        # If both values are numbers than evaluate condition and check whether
        # to perform condition of not
        if isinstance(self.x, Constant) and isinstance(self.y, Constant):
            code = [RESET(regc)]

            if self.eval_num() == 1:
                code += [INC(regc)]

            return code

        # If x is number than y is in memory
        if isinstance(self.x, Constant):
            pass

        # If y is number than x is in memory
        elif isinstance(self.y, Constant):
            pass

        # Otherwise both are in memory
        else:
            pass

        return []

class Equals(Condition):
    def eval_num(self):
        return 1 if self.x.value == self.y.value else 0

    def eval_mem(self, regx: str, regy: str):
        pass

class NotEquals(Condition):
    def eval_num(self):
        return 0 if self.x.value == self.y.value else 1

    def eval_mem(self, regx: str, regy: str):
        pass

class Lesser(Condition):
    def eval_num(self):
        return 1 if self.x.value < self.y.value else 0

    def eval_mem(self, regx: str, regy: str):
        pass

class Greater(Condition):
    def eval_num(self):
        return 1 if self.x.value > self.y.value else 0

    def eval_mem(self, regx: str, regy: str):
        pass

class LEQ(Condition):
    def eval_num(self):
        return 1 if self.x.value <= self.y.value else 0

    def eval_mem(self, regx: str, regy: str):
        pass

class GEQ(Condition):
    def eval_num(self):
        return 1 if self.x.value >= self.y.value else 0

    def eval_mem(self, regx: str, regy: str):
        pass
