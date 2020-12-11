from sly import Parser
from src.lexer import CompilerLexer

from src.variables import VariableManager
from src.blocks import Write, Assignment, operation_mapper
from src.program import Program

class CompilerParser(Parser):
    tokens = CompilerLexer.tokens

    # Program
    @_('BEGIN commands END')
    def program(self, p):
        return None

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        return None

    # Declarations
    @_('declarations COMMA PIDENTIFIER',
       'PIDENTIFIER'
    )
    def declarations(self, p):
        VariableManager.declare_variable(p.PIDENTIFIER, p.lineno)

    @_('declarations COMMA PIDENTIFIER LPARENT NUMBER COLON NUMBER RPARENT',
       'PIDENTIFIER LPARENT NUMBER COLON NUMBER RPARENT'
    )
    def declarations(self, p):
        VariableManager.declare_array(p.PIDENTIFIER, (p.NUMBER0, p.NUMBER1), p.lineno)

    # Commands
    @_('commands command',
       'command'
    )
    def commands(self, p):
        pass
    
    # Command
    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, p):
        Program.blocks.append(Assignment(p.identifier, p.expression, p.lineno))

    @_('WRITE value SEMICOLON')
    def command(self, p):
        Program.blocks.append(Write(p.value, p.lineno))

    @_('IF condition THEN commands ELSE commands ENDIF',
       'IF condition THEN commands ENDIF',
       'WHILE condition DO commands ENDWHILE',
       'REPEAT commands UNTIL condition SEMICOLON',
       'FOR PIDENTIFIER FROM value TO value DO commands ENDFOR',
       'FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR',
       'READ PIDENTIFIER SEMICOLON',
    )
    def command(self, p):
        pass
    
    # Expression
    @_('value',
       'value PLUS value',
       'value MINUS value',
       'value MULTIPLY value',
       'value DIVIDE value',
       'value MODULO value'
    )
    def expression(self, p):
        if len(p) == 1:
            return p.value
        else:
            return operation_mapper(p[1])(p.value0, p.value1, p.lineno)

    # Condition
    @_('value EQUALS value',
       'value NOT_EQUALS value',
       'value LESSER value',
       'value GREATER value',
       'value LEQ value',
       'value GEQ value'
    )
    def condition(self, p):
        pass

    # Value
    @_('NUMBER')
    def value(self, p):
        return p.NUMBER
    
    @_('identifier')
    def value(self, p):
        return p[0]

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
