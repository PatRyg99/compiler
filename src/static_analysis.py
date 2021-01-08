from typing import Union

from src.blocks import (
    Assignment,
    Constant,
    IfCondition,
    IfElseCondition,
    Write,
    Read,
    WhileLoop,
    RepeatUntilLoop,
    ForToLoop,
    ForDownToLoop,
    BinaryOperation,
    Condition,
)

from src.variables import Variable, UndeclaredIterator, ArrayElement


class StaticAnalyser:
    def __init__(self):
        self.variables = set()

    def is_cond_loop(self, block):
        return isinstance(block, RepeatUntilLoop) or isinstance(block, WhileLoop)

    def is_iter_loop(self, block):
        return isinstance(block, ForToLoop) or isinstance(block, ForDownToLoop)

    def add_variable(self, var):
        """Add variable to required"""
        if not isinstance(var, Constant):
            self.variables.add(var.name)

            if isinstance(var, ArrayElement):
                if isinstance(var.idx, Variable) or isinstance(
                    var.idx, UndeclaredIterator
                ):
                    self.variables.add(var.idx.name)

    def scan_variables(self, program):
        """Scan code for variables that are required"""
        if not isinstance(program, list):
            blocks = program.blocks
        else:
            blocks = program

        for block in reversed(blocks):

            # Write block
            if isinstance(block, Write):
                self.add_variable(block.x)

            # Iterator loop block
            elif self.is_iter_loop(block):
                self.scan_variables(block.commands)
                self.add_variable(block.start)
                self.add_variable(block.end)

            # Condition loop block
            elif self.is_cond_loop(block):
                self.scan_variables(block.commands)
                self.add_variable(block.condition.x)
                self.add_variable(block.condition.y)

            # If block
            elif isinstance(block, IfCondition):
                self.scan_variables(block.commands)
                self.add_variable(block.condition.x)
                self.add_variable(block.condition.y)

            # Else if block
            elif isinstance(block, IfElseCondition):
                self.scan_variables(block.if_commands)
                self.scan_variables(block.else_commands)
                self.add_variable(block.condition.x)
                self.add_variable(block.condition.y)

            # Assignment block
            elif isinstance(block, Assignment):

                # If required variable is being assigned
                # Add all expression variables to required
                if block.var.name in self.variables:
                    self.add_variable(block.var)
                    expr = block.expression

                    if isinstance(expr, BinaryOperation):
                        self.add_variable(expr.x)
                        self.add_variable(expr.y)

                    else:
                        self.add_variable(expr)

    def check_variable(self, var):
        """Check if block has required variable"""
        if not isinstance(var, Constant):
            if isinstance(var, ArrayElement):
                if isinstance(var.idx, ArrayElement) or isinstance(
                    var.idx, UndeclaredIterator
                ):
                    return var.name in self.variables or var.idx.name in self.variables

            return var.name in self.variables

        return False

    def remove_blocks(self, program):
        """Removing blocks from code that do not have required variables"""
        if not isinstance(program, list):
            blocks = program.blocks
        else:
            blocks = program

        for block in blocks:

            # Loop block
            if self.is_iter_loop(block) or self.is_cond_loop(block):
                self.remove_blocks(block.commands)

            # If block
            elif isinstance(block, IfCondition):
                self.remove_blocks(block.commands)

            # Else if block
            elif isinstance(block, IfElseCondition):
                self.remove_blocks(block.if_commands)
                self.remove_blocks(block.else_commands)

            # Assignment block
            elif isinstance(block, Assignment):

                if block.var.name not in self.variables:
                    block.generate = False

                    if not block.generate:
                        print("Removed block in line: ", block.lineno)

    def run(self, program):

        # Scan code for required variables
        self.scan_variables(program)
        print(self.variables)

        # Remove blocks with no required variables
        self.remove_blocks(program)

        return program
