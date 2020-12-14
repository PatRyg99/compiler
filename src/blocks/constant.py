from src.instructions import RESET, SHL, INC
from src.registers import RegisterManager, Register

class Constant:
    def __init__(self, value: int):
        self.value = value

    def generate_code(self, reg: str):

        # Reset operational register
        code = [RESET(reg)]

        # If value 0
        if self.value == 0:
            return code

        # Otherwise change to binary
        else:
            bin_value = bin(self.value)[2:]

            code.append(INC(reg))

            for bit in bin_value[1:]:
                code.append(SHL(reg))
                if bit == "1":
                    code.append(INC(reg))

        return code
