from src.errors import Error
from src.blocks.constant import Constant
from src.registers import RegisterManager
from src.instructions import (
    LOAD,
    ADD,
    SUB,
    RESET,
    JZERO,
    JUMP,
    DEC,
    INC,
    SHL,
    JODD,
    SHR,
)


def condition_mapper(operation: str):
    mapper = {
        "=": Equals,
        "!=": NotEquals,
        "<": Lesser,
        ">": Greater,
        "<=": LEQ,
        ">=": GEQ,
    }
    return mapper[operation]


class Condition:
    def __init__(self, x, y, lineno):
        self.x = x
        self.y = y
        self.lineno = lineno

    def eval_num(self):
        """Evaluate condition on constants"""
        raise NotImplementedError()

    def eval_mem(self, regx, regy):
        """Evaluate condition on memory registers"""
        raise NotImplementedError()

    def generate_code(self, regx):

        # If both values are numbers than evaluate condition and check whether
        # to perform condition of not
        if isinstance(self.x, Constant) and isinstance(self.y, Constant):
            code = [RESET(regx)]

            if self.eval_num() == 1:
                code += [INC(regx)]

            return code

        # Generate code for x variable
        x_code = self.x.generate_code(regx, self.lineno)

        # Generate code for y variable
        regy = RegisterManager.get_register()
        y_code = self.y.generate_code(regy, self.lineno)

        # Generating code
        code = x_code + y_code
        code += self.eval_mem(regx, regy)

        # Unlock y register
        regy.unlock()

        return code


class Equals(Condition):
    def eval_num(self):
        return 1 if self.x.value == self.y.value else 0

    def eval_mem(self, regx, regy):
        regz = RegisterManager.get_register()

        code = [
            # Copy x to z
            RESET(regz),
            ADD(regz, regx),
            # Perform substraction x - y
            SUB(regz, regy),
            JZERO(regz, 2),
            JUMP(9),
            # Copy y to z
            RESET(regz),
            ADD(regz, regy),
            # Perform substraction y - x
            SUB(regz, regx),
            JZERO(regz, 2),
            JUMP(4),
            # If both substractions are zero - EQUALS
            RESET(regx),
            INC(regx),
            JUMP(2),
            # Else not equals
            RESET(regx),
        ]

        regz.unlock()

        return code


class NotEquals(Condition):
    def eval_num(self):
        return 0 if self.x.value == self.y.value else 1

    def eval_mem(self, regx, regy):
        regz = RegisterManager.get_register()

        code = [
            # Copy x to z
            RESET(regz),
            ADD(regz, regx),
            # Perform substraction x - y
            SUB(regz, regy),
            JZERO(regz, 2),
            JUMP(8),
            # Copy y to z
            RESET(regz),
            ADD(regz, regy),
            # Perform substraction y - x
            SUB(regz, regx),
            JZERO(regz, 2),
            JUMP(3),
            # If both substractions are zero - EQUALS
            RESET(regx),
            JUMP(3),
            # Else not equals
            RESET(regx),
            INC(regx),
        ]

        regz.unlock()

        return code


class Lesser(Condition):
    def eval_num(self):
        return 1 if self.x.value < self.y.value else 0

    def eval_mem(self, regx, regy):
        code = [
            # Perform substraction and check if no 0
            SUB(regy, regx),
            JZERO(regy, 4),
            # If not zero return 1
            RESET(regx),
            INC(regx),
            JUMP(2),
            # Else return 0
            RESET(regx),
        ]

        return code


class Greater(Condition):
    def eval_num(self):
        return 1 if self.x.value > self.y.value else 0

    def eval_mem(self, regx, regy):
        code = [
            # Perform substraction and check if no 0
            SUB(regx, regy),
            JZERO(regx, 4),
            # If not zero return 1
            RESET(regx),
            INC(regx),
            JUMP(2),
            # Else return 0
            RESET(regx),
        ]

        return code


class LEQ(Lesser):
    def eval_num(self):
        return 1 if self.x.value <= self.y.value else 0

    def eval_mem(self, regx, regy):

        # x <= y <=> x < y + 1
        code = [INC(regy)]
        code += super().eval_mem(regx, regy)

        return code


class GEQ(Greater):
    def eval_num(self):
        return 1 if self.x.value >= self.y.value else 0

    def eval_mem(self, regx, regy):

        # x >= y <=> x + 1 > y
        code = [INC(regx)]
        code += super().eval_mem(regx, regy)

        return code
