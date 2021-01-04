class Block:
    def __init__(self, generate: bool = True):
        self.generate = generate

    def generate_code(self):
        raise NotImplementedError
