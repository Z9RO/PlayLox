from curses.ascii import isalpha, isdigit
from plox import error
from plox.token import Token, TokenType


def is_alpha(char: str) -> bool:
    return isalpha(char) or char == "_"


def is_digit_or_alpha(char: str) -> bool:
    return isdigit(char) or is_alpha(char)


keywords: dict[str, TokenType] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Scanner:
    source: str
    tokens: list[Token]
    start: int
    current: int
    line: int

    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scanToken()

        self.add_token(TokenType.EOF)
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scanToken(self) -> None:
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    while (self.peek() != "\n") and (not self.is_at_end()):
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case c if isdigit(c):
                self.number()
            case c if is_alpha(c):
                pass
            case c:
                error.error(self.line, f"Unexpected character: {c}.")

        pass

    def advance(self) -> str:
        current = self.current
        self.current += 1
        return self.source[current]

    def add_token(self, type: TokenType, literal: object = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        elif not self.source.startswith(expected):
            return False
        else:
            self.current += len(expected)
            return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\n"
        else:
            return self.source[self.current : self.current + 1]

    def peek_next(self) -> str:
        if (self.current + 1) >= len(self.source):
            return "\n"
        return self.source[self.current + 1 : self.current + 2]

    def string(self) -> None:
        while (self.peek() != '"') and (not self.is_at_end()):
            self.advance()

        if self.is_at_end():
            error.error(self.line, "Unterminated string.")

        # consume `"`
        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self) -> None:
        while isdigit(self.peek()):
            self.advance()

        if (self.peek() == ".") and (not isdigit(self.peek_next())):
            self.advance()
            while isdigit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self) -> None:
        while is_digit_or_alpha(self.peek()) or self.peek() == "_":
            self.advance()
        text = self.source[self.start : self.current]
        type = keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(type)
