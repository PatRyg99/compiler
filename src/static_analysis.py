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

    def run(self, program):

        if not isinstance(program, list):
            blocks = program.blocks
        else:
            blocks = program

        for block in reversed(blocks):
            if isinstance(block, Write):
                if not isinstance(block.x, Constant):
                    self.variables.add(block.x.name)

                    if isinstance(block.x, ArrayElement):
                        if isinstance(block.x.idx, ArrayElement) or isinstance(
                            block.x.idx, UndeclaredIterator
                        ):
                            self.variables.add(block.x.idx.name)

            elif self.is_iter_loop(block):
                # self.run(block.commands, delete=False)

                if not isinstance(block.start, Constant):
                    self.variables.add(block.start.name)

                if not isinstance(block.end, Constant):
                    self.variables.add(block.end.name)

            elif self.is_cond_loop(block):
                # self.run(block.commands, delete=False)
                cond = block.condition

                if not isinstance(cond.x, Constant):
                    self.variables.add(cond.x.name)

                if not isinstance(cond.y, Constant):
                    self.variables.add(cond.y.name)

            elif isinstance(block, IfCondition):
                self.run(block.commands)
                cond = block.condition

                if not isinstance(cond.x, Constant):
                    self.variables.add(cond.x.name)

                if not isinstance(cond.y, Constant):
                    self.variables.add(cond.y.name)

            elif isinstance(block, IfElseCondition):
                self.run(block.if_commands)
                self.run(block.else_commands)

                cond = block.condition

                if not isinstance(cond.x, Constant):
                    self.variables.add(cond.x.name)

                if not isinstance(cond.y, Constant):
                    self.variables.add(cond.y.name)

            # Check if block is assignment
            elif isinstance(block, Assignment):

                # If required variable is being assigned
                # Add all expression variables to required
                if block.var.name in self.variables:
                    expr = block.expression

                    if isinstance(expr, BinaryOperation):
                        if not isinstance(expr.x, Constant):
                            self.variables.add(expr.x.name)

                        if not isinstance(expr.y, Constant):
                            self.variables.add(expr.y.name)

                    elif not isinstance(expr, Constant):
                        self.variables.add(expr.name)

                # Otherwise set block to not be generated
                else:
                    block.generate = False

        return program
