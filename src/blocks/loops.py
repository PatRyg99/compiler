from src.instructions import JZERO, JUMP


class ConditionLoop:
    def __init__(self, condition, commands, lineno):
        self.condition = condition
        self.commands = commands
        self.lineno = lineno

        self.regs = ["a"]


class WhileLoop(ConditionLoop):
    def generate_code(self):

        # Generating condition evaluation to register regc
        regc = self.regs[0]
        cond_code = self.condition.generate_code(regc)

        # Generating code for loop
        loop_code = []
        for command in reversed(self.commands):
            loop_code += command.generate_code()

        # Adding jump to loop code
        loop_code += [JUMP(-(len(loop_code) + len(cond_code) + 1))]

        # Performing jump based on regc
        cond_code += [JZERO(regc, len(loop_code) + 1)]

        return cond_code + loop_code


class RepeatUntilLoop(ConditionLoop):
    def generate_code(self):

        # Generating condition evaluation to register regc
        regc = self.regs[0]
        cond_code = self.condition.generate_code(regc)

        # Generating code for loop
        loop_code = []
        for command in reversed(self.commands):
            loop_code += command.generate_code()

        # Performing jump based on regc
        cond_code += [JZERO(regc, -(len(loop_code) + len(cond_code)))]

        return loop_code + cond_code


class ForToLoop:
    pass


class ForDownToLoop:
    pass
