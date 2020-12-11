from src.instructions import *

class Constant:
    def __init__(self, value: int):
        self.value = value

    def generate_code(self, reg: str = "a"):
        code = [RESET(reg)]

        for _ in range(self.value):
            code.append(INC(reg))

        return code