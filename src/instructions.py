"""MEMORY OPERATIONS"""
def GET(m: int):
    return f"GET {m}"

def PUT(m: int):
    return f"PUT {m}"

"""REGISTER-MEMORY OPERATIONS"""
def LOAD(x: str, m: int):
    return f"LOAD {x} {m}"

def STORE(x: str, m: int):
    return f"STORE {x} {m}"

"""REGISTER OPERATIONS"""
def ADD(x: str, y: str):
    return f"ADD {x} {y}"

def SUB(x: str, y: str):
    return f"SUB {x} {y}"

def RESET(x: str):
    return f"RESET {x}"

def INC(x: str):
    return f"INC {x}"

def DEC(x: str):
    return f"DEC {x}"

def SHR(x: str):
    return f"SHR {x}"

def SHL(x: str):
    return f"SHL {x}"

"""JUMPING OPERATIONS"""
def JUMP(j: int):
    return f"JUMP {j}"

def JZERO(x: str, j: int):
    return f"JZERO {x} {j}"

def JODD(x: str, j: int):
    return f"JODD {x} {j}"

"""ENDING HALT OPERATION"""
def HALT():
    return "HALT"
