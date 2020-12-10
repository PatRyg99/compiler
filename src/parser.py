from sly import Parser
from src.lexer import CompilerLexer

from src.variables import VariableManager

class CompilerParser(Parser):
    tokens = CompilerLexer.tokens
    precedence = (
        ('left', "PLUS", "MINUS"),
        ('left', "MULTIPLY", "DIVIDE", "MODULO")
    )

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
    @_('identifier ASSIGN expression SEMICOLON',
       'IF condition THEN commands ELSE commands ENDIF',
       'IF condition THEN commands ENDIF',
       'WHILE condition DO commands ENDWHILE',
       'REPEAT commands UNTIL condition SEMICOLON',
       'FOR PIDENTIFIER FROM value TO value DO commands ENDFOR',
       'FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR',
       'READ PIDENTIFIER SEMICOLON',
       'WRITE PIDENTIFIER SEMICOLON'
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
        pass

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
    @_('NUMBER',
       'identifier'
    )
    def value(self, p):
        pass

    # Identifier
    @_('PIDENTIFIER',
       'PIDENTIFIER RPARENT PIDENTIFIER LPARENT',
       'PIDENTIFIER LPARENT NUMBER RPARENT'
    )
    def identifier(self, p):
        pass
