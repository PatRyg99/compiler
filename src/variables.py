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

        VariableManager.variables[name] = Variable(VariableManager.next_memory_block)
        VariableManager.next_memory_block += 1

    @staticmethod
    def declare_array(name: str, range: tuple, lineno: int):
        """Array declaration with name and range check"""
        VariableManager._check_redeclaration(name, lineno)
        length = VariableManager._compute_length(name, range, lineno)

        VariableManager.arrays[name] = Array(VariableManager.next_memory_block, range)
        VariableManager.next_memory_block += length

    @staticmethod
    def declare_iterator(name: str):
        """Iterator declaration"""
        VariableManager.iterators[name] = Iterator(VariableManager.next_memory_block)
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
    def __init__(self, memory_block: int):
        self.memory_block = memory_block
        self.initilized = False

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
    def __init__(self, memory_block: int, range: tuple, idx):
        self.memory_block = memory_block
        self.range = range
        self.idx = idx
        self.initilized = True

    def generate_mem(self, reg: str, lineno: int):

        # If index is a number - perform variable load
        if isinstance(self.idx, int):
            mem_block = self.memory_block + (self.idx - self.range[0])
            code = Constant(mem_block).generate_code(reg)

        # Otherwise index is a variable
        else:
            regv = RegisterManager.get_register()

            code = Constant(self.memory_block - self.range[0]).generate_code(reg)
            code += self.idx.generate_code(regv, lineno)

            code += [ADD(reg, regv)]

            regv.unlock()

        return code

    def generate_code(self, reg: str, lineno: int):

        code = self.generate_mem(reg, lineno)
        code.append(LOAD(reg, reg))

        return code


class Array:
    def __init__(self, memory_block: int, range: tuple):
        self.memory_block = memory_block
        self.range = range

    def get(self, idx: int, lineno: int):
        return ArrayElement(self.memory_block, self.range, idx)


class UndeclaredIterator:
    def __init__(self, name: str, lineno: int):
        self.name = name
        self.lineno = lineno

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
    def __init__(self, memory_block: int):
        self.memory_block = memory_block
        self.initilized = True

    def allocate_start(self, reg: str):
        mem = RegisterManager.get_register()

        code = Constant(self.memory_block).generate_code(mem)
        code.append(STORE(reg, mem))

        mem.unlock()

        return code

    def allocate_end(self, reg: str):
        mem = RegisterManager.get_register()

        code = Constant(self.memory_block + 1).generate_code(mem)
        code.append(STORE(reg, mem))

        mem.unlock()

        return code

    def increment(self, reg: str):
        regc = RegisterManager.get_register()

        code = Constant(self.memory_block).generate_code(reg)
        code += [LOAD(regc, reg), INC(regc), STORE(regc, reg)]

        regc.unlock()

        return code

    def decrement(self, reg):
        regc = RegisterManager.get_register()

        code = Constant(self.memory_block).generate_code(reg)
        code += [LOAD(regc, reg), JZERO(regc, 4), DEC(regc), STORE(regc, reg)]

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
