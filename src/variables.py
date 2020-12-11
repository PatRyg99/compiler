from src.instructions import *
from src.errors import (
    redeclaration_variable_error,
    variable_not_declared_error,
    variable_not_array_error, 
    array_invalid_range_error,
    array_invalid_index_error,
    array_not_indexed_error
)

class VariableManager:
    """VariableManager of arrays and variables"""
    variables = {}
    arrays = {}
    next_memory_block = 0

    @staticmethod
    def _check_redeclaration(name: str, lineno: int):
        """Check if variable hasn't been declared yet"""
        declared = list(VariableManager.variables.keys()) + list(VariableManager.arrays.keys())
        
        if name in declared:
            redeclaration_variable_error(name, lineno)

    @staticmethod
    def _compute_length(name: str, range: tuple, lineno: int):
        """Checking validity of array length and computing it"""
        length = range[1] - range[0] + 1

        if length <= 0:
            array_invalid_range_error(name, lineno)

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
    def get_var(name: str, lineno: int):
        """Getting variable by name"""
        try:
            return VariableManager.variables[name]

        except KeyError:
            if name not in VariableManager.arrays.keys():
                variable_not_declared_error(name, lineno)
            else:
                array_not_indexed_error(name, lineno)

    @staticmethod
    def get_array_element(name: str, lineno: int, idx: int):
        """Getting array element by name and index"""
        try:
            return VariableManager.arrays[name].get(idx, lineno, name)

        except KeyError:
            if name not in VariableManager.variables.keys():
                variable_not_declared_error(name, lineno)
            else:
                variable_not_array_error(name, lineno)

  
class Variable:
    def __init__(self, memory_block: int):
        self.memory_block = memory_block

class Array:
    def __init__(self, memory_block: int, range: tuple):
        self.memory_block = memory_block
        self.range = range

    def get(self, idx: int, lineno: int, name: str):
        if self.range[0] <= idx <= self.range[1]:
            mem_block = self.memory_block + (idx - self.range[0])
            return Variable(mem_block)

        else:
            array_invalid_index_error(lineno, name)
