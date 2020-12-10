from sly import Lexer
from src.errors import syntax_error

class CompilerLexer(Lexer):

    # List of tokens
    tokens = {
        PLUS, MINUS, MULTIPLY, DIVIDE, MODULO,
        EQUALS, NOT_EQUALS, LESSER, GREATER, LEQ, GEQ,
        COMMA, ASSIGN, COLON, SEMICOLON, LPARENT, RPARENT,
        DECLARE, BEGIN, END,
        IF, ELSE, THEN, ENDIF,
        WHILE, DO, ENDWHILE,
        REPEAT, UNTIL,
        FOR, FROM, TO, DOWNTO, ENDFOR,
        READ, WRITE,
        NUMBER, PIDENTIFIER
    }

    """IGNORED CHARACTERS"""
    # Ignore blank lines
    ignore_blank = r"[ \t]"

    # Ignore comment
    ignore_comment = r"\[.*\]"

    # Ignore newline and 
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
    EQUALS = r"="
    NOT_EQUALS = r"!="
    LESSER = r"<"
    GREATER = r">"
    LEQ = r"=<"
    GEQ = r">="   
    
    # Utility characters
    COMMA = r","
    ASSIGN = r":="
    COLON = r":"
    SEMICOLON = r";"
    LPARENT = r"\("
    RPARENT = r"\)"


    """LANGUAGE KEYWORDS"""
    # Program keywords
    DECLARE = r"DECLARE"
    BEGIN = r"BEGIN"
    END = r"END"

    # Conditional keywords
    IF = r"IF"
    ELSE = r"ELSE"
    THEN = r"THEN"
    ENDIF = r"ENDIF"

    # While loop keywords
    WHILE = r"WHILE"
    DO = r"DO"
    ENDWHILE = r"ENDWHILE"

    # Repeat until loop keywords
    REPEAT = r"REPEAT"
    UNTIL = r"UNTIL"
    
    # For loop keywords
    FOR = r"FOR"
    FROM = r"FROM"
    TO = r"TO"
    DOWNTO = r"DOWNTO"
    ENDFOR = r"ENDFOR"

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
        syntax_error(self.lineno)
