from src.errors import redeclaration_variable_error, array_invalid_range_error

class VariableManager:
    declared = []
    next_memory_block = 0

    @staticmethod
    def _check_redeclaration(name: str, lineno: int):
        for var in VariableManager.declared:
            if var.name == name:
                redeclaration_variable_error(name, lineno)

    @staticmethod
    def _compute_length(name: str, range: tuple, lineno: int):
        length = range[1] - range[0] + 1

        if length <= 0:
            array_invalid_range_error(name, lineno)

        return length
        
    @staticmethod
    def declare_variable(name: str, lineno: int):
        VariableManager._check_redeclaration(name, lineno)

        VariableManager.declared.append(Variable(name, VariableManager.next_memory_block))
        VariableManager.next_memory_block += 1

    @staticmethod
    def declare_array(name: str, range: tuple, lineno: int):
        VariableManager._check_redeclaration(name, lineno)
        length = VariableManager._compute_length(name, range, lineno)

        VariableManager.declared.append(Array(name, VariableManager.next_memory_block, range))
        VariableManager.next_memory_block += length

class Variable:
    def __init__(self, name: str, memory_block: int):
        self.name = name
        self.memory_block = memory_block

class Array:
    def __init__(self, name: str, memory_block: int, range: tuple):
        self.name = name
        self.memory_block = memory_block
        self.range = range