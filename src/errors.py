def syntax_error(line_number: int):
    _error(line_number, "Syntax error")

def redeclaration_variable_error(name: str, line_number: int):
    _error(line_number, f"Redeclaration of variable error ('{name}')")

def array_invalid_range_error(name: str, line_number: int):
    _error(line_number, f"Invalid range of array error ('{name}')")

def undeclared_variable_error(line_number: int):
    _error(line_number, "Undeclared variable error")

def _error(line_number: int, error_msg: str):
    print(f"[Line {line_number}]: {error_msg}")
    exit()
