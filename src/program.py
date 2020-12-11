class Program:
    blocks = []

    @staticmethod
    def generate_code():
        code = []

        for block in Program.blocks:
            block_code = block.generate_code()
            code += block_code

        return code