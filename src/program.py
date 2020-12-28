class Program:
    def __init__(self, blocks):
        self.blocks = blocks

    def generate_code(self):
        code = []

        for block in self.blocks:
            block_code = block.generate_code()
            code += block_code

        return code
