def condition_mapper(operation: str):
    mapper = {
        "=": Equals,
        "!=": NotEquals,
        "<": Lesser,
        ">": Greater,
        "<=": LEQ,
        ">=": GEQ
    }
    return mapper[operation]

class Condition:
    def __init__(self, x, y, lineno):
        self.x = x
        self.y = y
        self.lineno = lineno

        self.regs = ["a", "b"]

    def eval_num(self):
        """Evaluate condition on constants"""
        raise NotImplementedError()

    def eval_mem(self, regx: str, regy: str):
        """Evaluate condition on memory registers"""
        raise NotImplementedError()

    def generate_code(self, regx: str):
        pass

class Equals(Condition):
    pass

class NotEquals(Condition):
    pass

class Lesser(Condition):
    pass

class Greater(Condition):
    pass

class LEQ(Condition):
    pass

class GEQ(Condition):
    pass
