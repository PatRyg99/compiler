from src.instructions import ADD, LOAD, STORE, INC, DEC, RESET, JZERO
from src.blocks import Constant
from src.errors import Error
from src.registers import RegisterManager


class VariableManager:
    """VariableManager of arrays and variables"""

    variables = {}
    arrays = {}
    iterators = {}
    next_memory_block = 1

    @staticmethod
    def allocate():

        # Allocate variables
        for var in VariableManager.variables.values():
            var.memory_block = VariableManager.next_memory_block
            VariableManager.next_memory_block += 1

        # Allocate arrays
        for arr in VariableManager.arrays.values():
            arr.memory_block = VariableManager.next_memory_block
            VariableManager.next_memory_block += arr.range[1] - arr.range[0] + 1

    @staticmethod
    def _check_redeclaration(name: str, lineno: int):
        """Check if variable hasn't been declared yet"""
        declared = list(VariableManager.variables.keys()) + list(
            VariableManager.arrays.keys()
        )

        if name in declared:
            Error.VariableRedeclaration.throw(lineno)

    @staticmethod
    def _compute_length(name: str, range: tuple, lineno: int):
        """Checking validity of array length and computing it"""
        length = range[1] - range[0] + 1

        if length <= 0:
            Error.ArrayInvalidRange.throw(lineno)

        return length

    @staticmethod
    def declare_variable(name: str, lineno: int):
        """Variable declaration with name check"""
        VariableManager._check_redeclaration(name, lineno)
        VariableManager.variables[name] = Variable(name)

    @staticmethod
    def declare_array(name: str, range: tuple, lineno: int):
        """Array declaration with name and range check"""
        VariableManager._check_redeclaration(name, lineno)
        VariableManager._compute_length(name, range, lineno)
        VariableManager.arrays[name] = Array(name, range)

    @staticmethod
    def declare_iterator(name: str):
        """Iterator declaration"""
        VariableManager.iterators[name] = Iterator(
            name, VariableManager.next_memory_block
        )
        VariableManager.next_memory_block += 2

    @staticmethod
    def get_var(name: str, lineno: int):
        """Getting variable by name"""
        try:
            if name in VariableManager.iterators.keys():
                return VariableManager.iterators[name]
            else:
                return VariableManager.variables[name]

        except KeyError:
            if name not in VariableManager.arrays.keys():
                return UndeclaredIterator(name, lineno)
            else:
                Error.ArrayNotIndexed.throw(lineno)

    @staticmethod
    def get_array_element(name: str, lineno: int, idx: int):
        """Getting array element by name and index"""
        try:
            return VariableManager.arrays[name].get(idx, lineno)

        except KeyError:
            if name not in VariableManager.variables.keys():
                Error.VariableNotDeclared.throw(lineno)
            else:
                Error.IndexedVariableNotArray.throw(lineno)


class Variable:
    def __init__(self, name: str):
        self.name = name
        self.memory_block = None
        self.initilized = False

        self.used_regs = 0

    def generate_mem(self, reg: str, lineno: int):
        if self.initilized:
            return Constant(self.memory_block).generate_code(reg)
        else:
            Error.VariableNotInitialized.throw(lineno)

    def generate_code(self, reg: str, lineno: int):
        code = self.generate_mem(reg, lineno)
        code.append(LOAD(reg, reg))

        return code


class ArrayElement:
    def __init__(self, name: str, range: tuple, idx):
        self.name = name
        self.range = range
        self.idx = idx
        self.initilized = True
        self.memory_block = None

        self.used_regs = 0

    def generate_mem(self, reg: str, lineno: int):

        # Get memory block from parent array
        self.memory_block = VariableManager.arrays[self.name].memory_block

        # If index is a number - perform variable load
        if isinstance(self.idx, int):
            mem_block = self.memory_block + (self.idx - self.range[0])
            code = Constant(mem_block).generate_code(reg)

        # Otherwise index is a variable
        else:
            regv = RegisterManager.get_register()
            self.used_regs = 1

            code = Constant(self.memory_block - self.range[0]).generate_code(reg)
            code += self.idx.generate_code(regv, lineno)
            self.used_regs += self.idx.used_regs

            code += [ADD(reg, regv)]

            regv.unlock()

        return code

    def generate_code(self, reg: str, lineno: int):

        code = self.generate_mem(reg, lineno)
        code.append(LOAD(reg, reg))

        return code


class Array:
    def __init__(self, name: str, range: tuple):
        self.name = name
        self.range = range
        self.memory_block = None

        self.used_regs = 0

    def get(self, idx: int, lineno: int):
        return ArrayElement(self.name, self.range, idx)


class UndeclaredIterator:
    def __init__(self, name: str, lineno: int):
        self.name = name
        self.lineno = lineno

        self.used_regs = 0

    def declare(self):
        if self.name in VariableManager.iterators.keys():
            return VariableManager.iterators[self.name]
        else:
            Error.VariableNotDeclared.throw(self.lineno)

    def generate_mem(self, reg: str, lineno: int):
        return self.declare().generate_mem(reg, lineno)

    def generate_code(self, reg: str, lineno: int):
        return self.declare().generate_code(reg, lineno)


class Iterator:
    def __init__(self, name: str, memory_block: int):
        self.name = name
        self.memory_block = memory_block
        self.initilized = True

        self.used_regs = 0

    def allocate_range(self, reg_start: str, reg_end: str):
        mem = RegisterManager.get_register()
        self.used_regs = 1

        code = Constant(self.memory_block).generate_code(mem)
        code += [STORE(reg_start, mem), INC(mem), STORE(reg_end, mem)]

        mem.unlock()

        return code

    def increment(self, mem_reg: str = None):
        regc = RegisterManager.get_register()
        self.used_regs = 1

        code = []

        if not mem_reg:
            mem_reg = RegisterManager.get_register()
            self.used_regs += 1

            code = Constant(self.memory_block).generate_code(mem_reg)
            mem_reg.unlock()

        code += [LOAD(regc, mem_reg), INC(regc), STORE(regc, mem_reg)]
        regc.unlock()

        return code

    def decrement(self, mem_reg: str = None):
        regc = RegisterManager.get_register()
        self.used_regs = 1

        code = []

        if not mem_reg:
            mem_reg = RegisterManager.get_register()

            self.used_regs += 1
            code = Constant(self.memory_block).generate_code(mem_reg)

            mem_reg.unlock()

        code += [LOAD(regc, mem_reg), JZERO(regc, 4), DEC(regc), STORE(regc, mem_reg)]

        regc.unlock()

        return code

    def generate_end_code(self, reg):
        code = Constant(self.memory_block + 1).generate_code(reg)
        code.append(LOAD(reg, reg))

        return code

    def generate_mem(self, reg, lineno: int):
        return Constant(self.memory_block).generate_code(reg)

    def generate_code(self, reg, lineno: int):
        code = self.generate_mem(reg, lineno)
        code.append(LOAD(reg, reg))

        return code

    def generate_both(self, reg, reg_end, lineno: int):
        code = self.generate_mem(reg_end, lineno)
        code += [LOAD(reg, reg_end), INC(reg_end), LOAD(reg_end, reg_end)]

        return code
