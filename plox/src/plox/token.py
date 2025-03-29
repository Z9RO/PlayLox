from enum import Enum, auto


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = (auto(),)
    RIGHT_PAREN = (auto(),)
    LEFT_BRACE = (auto(),)
    RIGHT_BRACE = (auto(),)
    COMMA = (auto(),)
    DOT = (auto(),)
    MINUS = (auto(),)
    PLUS = (auto(),)
    SEMICOLON = (auto(),)
    SLASH = (auto(),)
    STAR = (auto(),)

    # One or two character tokens.
    BANG = (auto(),)
    BANG_EQUAL = (auto(),)
    EQUAL = (auto(),)
    EQUAL_EQUAL = (auto(),)
    GREATER = (auto(),)
    GREATER_EQUAL = (auto(),)
    LESS = (auto(),)
    LESS_EQUAL = (auto(),)

    # Literals.
    IDENTIFIER = (auto(),)
    STRING = (auto(),)
    NUMBER = (auto(),)

    # Keywords.
    AND = (auto(),)
    CLASS = (auto(),)
    ELSE = (auto(),)
    FALSE = (auto(),)
    FUN = (auto(),)
    FOR = (auto(),)
    IF = (auto(),)
    NIL = (auto(),)
    OR = (auto(),)
    PRINT = (auto(),)
    RETURN = (auto(),)
    SUPER = (auto(),)
    THIS = (auto(),)
    TRUE = (auto(),)
    VAR = (auto(),)
    WHILE = (auto(),)

    EOF = (auto(),)


class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type.name} {self.lexeme} {self.literal}"
