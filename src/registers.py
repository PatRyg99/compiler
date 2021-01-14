from enum import Enum


class Register:
    def __init__(self, name: str):
        self.name = name
        self.lock = False

    def unlock(self):
        self.lock = False

    def __str__(self):
        return self.name


class RegisterManager:
    registers = [Register(x) for x in "abcdef"]
    max_locked = 0

    @staticmethod
    def reset_max():
        RegisterManager.max_locked = 0

    @staticmethod
    def get_register_by_id(id: int):
        reg = RegisterManager.registers[id]
        reg.lock = True

        return reg

    @staticmethod
    def get_register():
        free_regs = [reg for reg in RegisterManager.registers if not reg.lock]
        reg = sorted(free_regs, key=lambda x: x.name)[0]
        reg.lock = True

        RegisterManager.max_locked = max(
            RegisterManager.max_locked,
            len(RegisterManager.registers) - len(free_regs) + 1,
        )

        return reg
