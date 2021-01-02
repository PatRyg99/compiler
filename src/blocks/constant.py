from src.instructions import RESET, SHL, INC


class Constant:
    def __init__(self, value: int):
        self.value = value

    def generate_code(self, reg, lineno: int = None):

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
