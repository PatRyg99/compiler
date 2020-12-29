# pylint: skip-file
# flake8: noqa
# fmt: off
from sly import Lexer
from src.errors import Error

class CompilerLexer(Lexer):

    # List of tokens
    tokens = {
        PLUS, MINUS, MULTIPLY, DIVIDE, MODULO,
        LEQ, GEQ, EQUALS, NOT_EQUALS, LESSER, GREATER,
        COMMA, ASSIGN, COLON, SEMICOLON, LPARENT, RPARENT,
        IF, ELSE, THEN, ENDIF,
        WHILE, DO, ENDWHILE,
        REPEAT, UNTIL,
        FOR, FROM, TO, DOWNTO, ENDFOR,
        DECLARE, BEGIN, END,
        READ, WRITE,
        NUMBER, PIDENTIFIER,
    }

    """IGNORED CHARACTERS"""
    # Ignore blank lines
    ignore_blank = r"[ \t]"

    # Ignore comment
    ignore_comment = r"\[(.|\n)*?\]"

    # Ignore newline
    @_(r'\n')
    def ignore_newline(self, t):
        self.lineno += len(t.value)


    """OPERANDS AND UTILITY CHARACTERS"""
    # Math operands
    PLUS = r"\+"
    MINUS = r"-"
    MULTIPLY = r"\*"
    DIVIDE = r"\/"
    MODULO = r"%"

    # Conditional operands keywords
    LEQ = r"<="
    GEQ = r">="
    EQUALS = r"="
    NOT_EQUALS = r"!="
    LESSER = r"<"
    GREATER = r">"

    # Utility characters
    COMMA = r","
    ASSIGN = r":="
    COLON = r":"
    SEMICOLON = r";"
    LPARENT = r"\("
    RPARENT = r"\)"


    """LANGUAGE KEYWORDS"""
    # Conditional keywords
    ENDIF = r"ENDIF"
    IF = r"IF"
    ELSE = r"ELSE"
    THEN = r"THEN"

    # For loop keywords
    FOR = r"FOR"
    FROM = r"FROM"
    TO = r"TO"
    DOWNTO = r"DOWNTO"
    ENDFOR = r"ENDFOR"

    # While loop keywords
    WHILE = r"WHILE"
    DO = r"DO"
    ENDWHILE = r"ENDWHILE"

    # Repeat until loop keywords
    REPEAT = r"REPEAT"
    UNTIL = r"UNTIL"
    
    # Program keywords
    DECLARE = r"DECLARE"
    BEGIN = r"BEGIN"
    END = r"END"

    # IO stream keywords
    READ = r"READ"
    WRITE = r"WRITE"


    """VARIABLES NAMES AND NUMBERS"""
    # Identifier regex
    PIDENTIFIER = r"[_a-z]+"

    # Number regex with conversion
    @_(r"\d+")
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    """ERROR HANDLING"""
    # Error handling on other characters
    def error(self, t):
        Error.Syntax.throw(self.lineno)
