class Register:
    def __init__(self):
        self.value = None
        self.locked = False
        self.iterator = False

class RegisterManager:
    a = Register()
    b = Register()
    c = Register()
    d = Register()
    e = Register()
    f = Register()
