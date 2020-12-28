# pylint: skip-file
from sly import Parser
from src.lexer import CompilerLexer

from src.variables import VariableManager
from src.program import Program
from src.blocks import (
    Write,
    Assignment,
    Constant,
    IfCondition,
    IfElseCondition,
    operation_mapper,
    condition_mapper
)


class CompilerParser(Parser):
    tokens = CompilerLexer.tokens

    ################# PROGRAM ###################
    @_('BEGIN commands END')
    def program(self, p):
        return Program(reversed(p.commands))

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        return Program(reversed(p.commands))


    ################ DECLARTIONS ###############
    @_('declarations COMMA PIDENTIFIER',
       'PIDENTIFIER'
    )
    def declarations(self, p):
        VariableManager.declare_variable(p.PIDENTIFIER, p.lineno)
        return None

    @_('declarations COMMA PIDENTIFIER LPARENT NUMBER COLON NUMBER RPARENT',
       'PIDENTIFIER LPARENT NUMBER COLON NUMBER RPARENT'
    )
    def declarations(self, p):
        VariableManager.declare_array(p.PIDENTIFIER, (p.NUMBER0, p.NUMBER1), p.lineno)
        return None


    ############### COMMANDS ################
    @_('commands command')
    def commands(self, p):
        return [p.command] + p.commands

    @_('command')
    def commands(self, p):
        return [p.command]
    
    # Assignment
    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, p):
        return Assignment(p.identifier, p.expression, p.lineno)

    # Write
    @_('WRITE value SEMICOLON')
    def command(self, p):
        return Write(p.value, p.lineno)

    # Else if
    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return IfElseCondition(p.condition, p.commands0, p.commands1, p.lineno)

    # If
    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return IfCondition(p.condition, p.commands, p.lineno)

    @_('WHILE condition DO commands ENDWHILE',
       'REPEAT commands UNTIL condition SEMICOLON',
       'FOR PIDENTIFIER FROM value TO value DO commands ENDFOR',
       'FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR',
       'READ PIDENTIFIER SEMICOLON',
    )
    def command(self, p):
        pass
    

    ################## EXPRESSIONS ####################
    @_('value')
    def expression(self, p):
        return p.value

    # Arithmentic
    @_('value PLUS value',
       'value MINUS value',
       'value MULTIPLY value',
       'value DIVIDE value',
       'value MODULO value'
    )
    def expression(self, p):
        return operation_mapper(p[1])(p.value0, p.value1, p.lineno)

    # Logical
    @_('value EQUALS value',
       'value NOT_EQUALS value',
       'value LESSER value',
       'value GREATER value',
       'value LEQ value',
       'value GEQ value'
    )
    def condition(self, p):
        return condition_mapper(p[1])(p.value0, p.value1, p.lineno)

    # Value
    @_('NUMBER')
    def value(self, p):
        return Constant(p.NUMBER)
    
    @_('identifier')
    def value(self, p):
        return p.identifier

    # Identifier
    @_('PIDENTIFIER')
    def identifier(self, p):
        return VariableManager.get_var(p.PIDENTIFIER, p.lineno)

    @_('PIDENTIFIER LPARENT PIDENTIFIER RPARENT')
    def identifier(self, p):
        return None

    @_('PIDENTIFIER LPARENT NUMBER RPARENT')
    def identifier(self, p):
        return VariableManager.get_array_element(p.PIDENTIFIER, p.lineno, p.NUMBER)
