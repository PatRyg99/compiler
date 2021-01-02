from src.instructions import JZERO, JUMP, RESET, ADD, LOAD, INC, DEC, SUB
from src.blocks import Constant
from src.blocks.conditions import LEQ, GEQ
from src.registers import RegisterManager


class ConditionLoop:
    def __init__(self, condition, commands, lineno):
        self.condition = condition
        self.commands = commands
        self.lineno = lineno


class WhileLoop(ConditionLoop):
    def generate_code(self):

        # Generating condition evaluation to register regc
        regc = RegisterManager.get_register()
        cond_code = self.condition.generate_code(regc)
        regc.unlock()

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
        regc = RegisterManager.get_register()
        cond_code = self.condition.generate_code(regc)
        regc.unlock()

        # Generating code for loop
        loop_code = []
        for command in reversed(self.commands):
            loop_code += command.generate_code()

        # Performing jump based on regc
        cond_code += [JZERO(regc, -(len(loop_code) + len(cond_code)))]

        return loop_code + cond_code


class IteratorLoop:
    def __init__(self, iter_name, start, end, commands, lineno):
        self.iter_name = iter_name
        self.start = start
        self.end = end
        self.commands = commands
        self.lineno = lineno

    def declare_iter(self):
        from src.variables import VariableManager

        reg = RegisterManager.get_register()

        # Compute starting value
        if isinstance(self.start, Constant):
            start_code = self.start.generate_code(reg)
        else:
            start_code = self.start.generate_mem(reg, self.lineno)
            start_code.append(LOAD(reg, reg))

        # Compute ending value
        if isinstance(self.end, Constant):
            end_code = self.end.generate_code(reg)
        else:
            end_code = self.end.generate_mem(reg, self.lineno)
            end_code.append(LOAD(reg, reg))

        # Allocate iterator with constant range
        VariableManager.declare_iterator(self.iter_name)
        start_code += VariableManager.iterators[self.iter_name].allocate_start(reg)
        end_code += VariableManager.iterators[self.iter_name].allocate_end(reg)

        reg.unlock()

        return start_code + end_code

    def undeclare_iter(self):
        from src.variables import VariableManager

        del VariableManager.iterators[self.iter_name]
        VariableManager.next_memory_block -= 2


class ForToLoop(IteratorLoop):
    def generate_code(self):
        from src.variables import VariableManager

        # Code for iterator declaration
        iter_code = self.declare_iter()
        iterator = VariableManager.iterators[self.iter_name]

        # Check iter condition
        iter_reg = RegisterManager.get_register()
        cond_reg = RegisterManager.get_register()

        cond_code = iterator.generate_code(iter_reg, self.lineno)
        cond_code += iterator.generate_end_code(cond_reg)

        cond_code += [
            # Check LEQ
            INC(cond_reg),
            SUB(cond_reg, iter_reg),
        ]

        iter_reg.unlock()
        cond_reg.unlock()

        # Generating code for loop
        loop_code = []
        for command in reversed(self.commands):
            loop_code += command.generate_code()

        # Perform increment
        iter_reg = RegisterManager.get_register()
        cond_reg = RegisterManager.get_register()

        # Increment iter and jump
        inc_code = iterator.increment(iter_reg)
        inc_code += [JUMP(-(len(cond_code) + len(loop_code) + len(inc_code) + 1))]

        # Add jump to condition
        cond_code.append(JZERO(cond_reg, len(inc_code) + len(loop_code) + 1))

        # Undeclare iterator
        self.undeclare_iter()

        iter_reg.unlock()
        cond_reg.unlock()

        return iter_code + cond_code + loop_code + inc_code


class ForDownToLoop(IteratorLoop):
    def generate_code(self):
        from src.variables import VariableManager

        # Code for interator declarion
        iter_code = self.declare_iter()
        iterator = VariableManager.iterators[self.iter_name]

        # Check iter condition
        iter_reg = RegisterManager.get_register()
        cond_reg = RegisterManager.get_register()

        cond_code = iterator.generate_code(iter_reg, self.lineno)
        cond_code += iterator.generate_end_code(cond_reg)
        cond_code += [
            # Check GEQ
            INC(iter_reg),
            SUB(iter_reg, cond_reg),
        ]

        # Generating code for loop
        loop_code = []
        for command in reversed(self.commands):
            loop_code += command.generate_code()

        # Perform decrement
        iter_reg = RegisterManager.get_register()
        cond_reg = RegisterManager.get_register()

        # Decrement iter and jump
        dec_code = iterator.decrement(iter_reg)
        dec_code += [JUMP(-(len(cond_code) + len(loop_code) + len(dec_code) + 1))]

        # Add jump to condition
        cond_code.append(JZERO(iter_reg, len(dec_code) + len(loop_code) + 1))

        # Undeclare iterator
        self.undeclare_iter()

        iter_reg.unlock()
        cond_reg.unlock()

        return iter_code + cond_code + loop_code + dec_code
