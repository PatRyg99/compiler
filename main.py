import argparse
from src.lexer import CompilerLexer
from src.parser import CompilerParser
from src.variables import VariableManager
from src.program import Program
from src.static_analysis import StaticAnalyser
from src.registers import RegisterManager


def main(in_file: str, out_file: str):

    with open(in_file, "r") as f:
        data = f.read()

    # Defining lexer and parser
    lexer = CompilerLexer()
    parser = CompilerParser()

    # Running lexer and parser
    tokens = lexer.tokenize(data)
    program = parser.parse(tokens)

    # Allocating variables
    VariableManager.allocate()

    # Performing static analysis
    program = StaticAnalyser().run(program)

    if program is not None:
        code = program.generate_code()

        with open(out_file, "w") as f:
            code.append("HALT")
            f.write("\n".join(code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("out_file")

    args = parser.parse_args()
    main(**vars(args))
