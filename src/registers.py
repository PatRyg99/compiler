class Register:
    def __init__(self, name: str):
        self.name = name
        self.value = None
        self.locked = False
        self.iterator = False

    def unlock(self):
        self.locked = False

class RegisterManager:
    registers = {
        "a": Register("a"),
        "b": Register("b"),
        "c": Register("c"),
        "d": Register("d"),
        "e": Register("e"),
        "f": Register("f")
    }

    @staticmethod
    def get_free_register():
        for reg in RegisterManager.registers.values():
            if not reg.locked:
                reg.locked = True
                return reg
