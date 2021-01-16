class Register:
    def __init__(self, name: str):
        self.name = name
        self.value = None

        self.lock = False

    def unlock(self):
        self.lock = False

    def __str__(self):
        return self.name


class RegisterManager:
    registers = [Register(x) for x in "abcdef"]

    @staticmethod
    def get_register(var: str = None, value: int = None):
        for reg in RegisterManager.registers:
            if not reg.lock:
                reg.lock = True
                return reg
