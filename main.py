import argparse
from src.lexer import CompilerLexer
from src.parser import CompilerParser
from src.variables import VariableManager

def main(in_file: str, out_file: str):

    with open(in_file, "r") as f:
        data = f.read()
    
    lexer = CompilerLexer()
    parser = CompilerParser()

    tokens = lexer.tokenize(data)
    res = parser.parse(tokens)

    for var in VariableManager.declared:
        if not hasattr(var, "range"):
            print(f"[Variable] Name: {var.name}, Mem: {var.memory_block}")
        else:
            print(f"[Array] Name: {var.name}, Mem: {var.memory_block}, Range: {var.range}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("out_file")

    args = parser.parse_args()
    main(**vars(args))