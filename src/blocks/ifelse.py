from src.blocks import Block
from src.instructions import JZERO, JUMP
from src.registers import RegisterManager


class IfCondition(Block):
    def __init__(self, condition, commands, lineno):
        super().__init__()

        self.condition = condition
        self.commands = commands
        self.lineno = lineno

        self.used_regs = 0

    def generate_code(self):

        # Generating condition evaluation to register regc
        regc = RegisterManager.get_register()
        cond_code = self.condition.generate_code(regc)

        self.used_regs = 1 + RegisterManager.max_locked
        RegisterManager.reset_max()
        regc.unlock()

        # Generating code for if condition
        if_code = []
        for command in self.commands:
            if command.generate:
                if_code += command.generate_code()
                self.used_regs = max(self.used_regs, command.used_regs)

        # If no if code inside - omit if generation
        if not if_code:
            return []

        # Performing jump based on regc
        cond_code += [JZERO(regc, len(if_code) + 1)]

        return cond_code + if_code


class IfElseCondition(Block):
    def __init__(self, condition, if_commands, else_commands, lineno):
        super().__init__()

        self.condition = condition
        self.if_commands = if_commands
        self.else_commands = else_commands
        self.lineno = lineno

        self.used_regs = 0

    def generate_code(self):
        regc = RegisterManager.get_register()
        cond_code = self.condition.generate_code(regc)

        self.used_regs = 1 + RegisterManager.max_locked
        RegisterManager.reset_max()
        regc.unlock()

        # Generating code for if condition
        if_code = []
        for command in self.if_commands:
            if command.generate:
                if_code += command.generate_code()
                self.used_regs = max(self.used_regs, command.used_regs)

        # Generating code for else condition
        else_code = []
        for command in self.else_commands:
            if command.generate:
                else_code += command.generate_code()
                self.used_regs = max(self.used_regs, command.used_regs)

        # If no if and else code inside - omit ifelse generation
        if not if_code and not else_code:
            return []

        # Omitting else if condition is true
        if_code += [JUMP(len(else_code) + 1)]

        # Performing jump based on regc
        cond_code += [JZERO(regc, len(if_code) + 1)]

        return cond_code + if_code + else_code
