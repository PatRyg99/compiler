def syntax_error(line_number: int):
    _error(line_number, "Syntax error")

def undeclared_variable_error(line_number: int):
    _error(line_number, "Undeclared variable error")

def redeclaration_variable_error(name: str, line_number: int):
    _error(line_number, f"Redeclaration of variable error ('{name}')")

def array_invalid_range_error(name: str, line_number: int):
    _error(line_number, f"Invalid range of array error ('{name}')")

def array_invalid_index_error(name: str, line_number: int):
    _error(line_number, f"Invalid array index error ('{name}')")

def array_not_indexed_error(name: str, line_number: int):
    _error(line_number, f"Array not indexed error ('{name}')")

def variable_not_array_error(name: str, line_number: int):
    _error(line_number, f"Indexed variable error - '{name}' is not an array")

def variable_not_declared_error(name: str, line_number: int):
    _error(line_number, f"Variable not declared error ('{name}')")

def division_by_zero_error(line_number: int):
    _error(line_number, "Division by zero error")


def _error(line_number: int, error_msg: str):
    print(f"[Line {line_number}]: {error_msg}")
    exit()
