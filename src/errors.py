from enum import Enum


class Error(Enum):
    Syntax = 0
    UndeclaredVariable = 1
    VariableRedeclaration = 2
    ArrayInvalidRange = 3
    ArrayNotIndexed = 4
    VariableNotDeclared = 5
    IndexedVariableNotArray = 6
    VariableNotInitialized = 7
    IteratorModification = 8

    def throw(self, lineno: int):
        print(f"[Line {lineno}] Error: {self.name}")
        exit()
