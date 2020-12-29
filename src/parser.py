# pylint: skip-file
# flake8: noqa
from sly import Parser
from src.lexer import CompilerLexer

from src.variables import VariableManager
from src.program import Program
from src.blocks import (
    Assignment,
    Constant,
    IfCondition,
    IfElseCondition,
    WhileLoop,
    RepeatUntilLoop,
    ForToLoop,
    ForDownToLoop,
    Write,
    Read,
    operation_mapper,
    condition_mapper,
)


class CompilerParser(Parser):
    tokens = CompilerLexer.tokens

    ################# PROGRAM ###################
    @_("BEGIN commands END")
    def program(self, p):
        return Program(reversed(p.commands))

    @_("DECLARE declarations BEGIN commands END")
    def program(self, p):
        return Program(reversed(p.commands))

    ################ DECLARTIONS ###############
    @_("declarations COMMA PIDENTIFIER", "PIDENTIFIER")
    def declarations(self, p):
        VariableManager.declare_variable(p.PIDENTIFIER, p.lineno)

    @_(
        "declarations COMMA PIDENTIFIER LPARENT NUMBER COLON NUMBER RPARENT",
        "PIDENTIFIER LPARENT NUMBER COLON NUMBER RPARENT",
    )
    def declarations(self, p):
        VariableManager.declare_array(p.PIDENTIFIER, (p.NUMBER0, p.NUMBER1), p.lineno)

    ############### COMMANDS ################
    @_("commands command")
    def commands(self, p):
        return [p.command] + p.commands

    @_("command")
    def commands(self, p):
        return [p.command]

    # Assignment
    @_("identifier ASSIGN expression SEMICOLON")
    def command(self, p):
        return Assignment(p.identifier, p.expression, p.lineno)

    # Write
    @_("WRITE value SEMICOLON")
    def command(self, p):
        return Write(p.value, p.lineno)

    # Read
    @_("READ PIDENTIFIER SEMICOLON")
    def command(self, p):
        var = VariableManager.get_var(p.PIDENTIFIER, p.lineno)
        return Read(var, p.lineno)

    # Else if condition
    @_("IF condition THEN commands ELSE commands ENDIF")
    def command(self, p):
        return IfElseCondition(p.condition, p.commands0, p.commands1, p.lineno)

    # If condition
    @_("IF condition THEN commands ENDIF")
    def command(self, p):
        return IfCondition(p.condition, p.commands, p.lineno)

    # While loop
    @_("WHILE condition DO commands ENDWHILE")
    def command(self, p):
        return WhileLoop(p.condition, p.commands, p.lineno)

    # Repeat until loop
    @_("REPEAT commands UNTIL condition SEMICOLON")
    def command(self, p):
        return RepeatUntilLoop(p.condition, p.commands, p.lineno)

    # For loop
    @_("FOR PIDENTIFIER FROM value TO value DO commands ENDFOR")
    def command(self, p):
        return ForToLoop(p.PIDENTIFIER, p.value0, p.value1, p.commands, p.lineno)

    @_("FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR")
    def command(self, p):
        return ForDownToLoop(p.PIDENTIFIER, p.value0, p.value1, p.commands, p.lineno)

    ################## EXPRESSIONS ####################
    @_("value")
    def expression(self, p):
        return p.value

    # Arithmentic
    @_(
        "value PLUS value",
        "value MINUS value",
        "value MULTIPLY value",
        "value DIVIDE value",
        "value MODULO value",
    )
    def expression(self, p):
        return operation_mapper(p[1])(p.value0, p.value1, p.lineno)

    # Logical
    @_(
        "value EQUALS value",
        "value NOT_EQUALS value",
        "value LESSER value",
        "value GREATER value",
        "value LEQ value",
        "value GEQ value",
    )
    def condition(self, p):
        return condition_mapper(p[1])(p.value0, p.value1, p.lineno)

    # Value
    @_("NUMBER")
    def value(self, p):
        return Constant(p.NUMBER)

    @_("identifier")
    def value(self, p):
        return p.identifier

    # Identifier
    @_("PIDENTIFIER")
    def identifier(self, p):
        return VariableManager.get_var(p.PIDENTIFIER, p.lineno)

    @_("PIDENTIFIER LPARENT PIDENTIFIER RPARENT")
    def identifier(self, p):
        var = VariableManager.get_var(p.PIDENTIFIER1, p.lineno)
        return VariableManager.get_array_element(p.PIDENTIFIER0, p.lineno, var)

    @_("PIDENTIFIER LPARENT NUMBER RPARENT")
    def identifier(self, p):
        return VariableManager.get_array_element(p.PIDENTIFIER, p.lineno, p.NUMBER)
