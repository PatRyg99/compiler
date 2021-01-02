from src.instructions import JZERO, JUMP


class IfCondition:
    def __init__(self, condition, commands, lineno):
        self.condition = condition
        self.commands = commands
        self.lineno = lineno

        self.regs = ["a"]

    def generate_code(self):

        # Generating condition evaluation to register regc
        regc = self.regs[0]
        cond_code = self.condition.generate_code(regc)

        # Generating code for if condition
        if_code = []
        for command in reversed(self.commands):
            if_code += command.generate_code()

        # Performing jump based on regc
        cond_code += [JZERO(regc, len(if_code) + 1)]

        return cond_code + if_code


class IfElseCondition:
    def __init__(self, condition, if_commands, else_commands, lineno):
        self.condition = condition
        self.if_commands = if_commands
        self.else_commands = else_commands
        self.lineno = lineno

        self.regs = ["a"]

    def generate_code(self):
        regc = self.regs[0]
        cond_code = self.condition.generate_code(regc)

        # Generating code for if condition
        if_code = []
        for command in reversed(self.if_commands):
            if_code += command.generate_code()

        # Generating code for else condition
        else_code = []
        for command in reversed(self.else_commands):
            else_code += command.generate_code()

        # Omitting else if condition is true
        if_code += [JUMP(len(else_code) + 1)]

        # Performing jump based on regc
        cond_code += [JZERO(regc, len(if_code) + 1)]

        return cond_code + if_code + else_code
