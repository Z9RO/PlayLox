from curses.ascii import isalpha, isdigit
from plox import error
from plox.token import Token, TokenType


def is_alpha(char: str) -> bool:
    return isalpha(char) or char == "_"


def is_digit_or_alpha(char: str) -> bool:
    return isdigit(char) or is_alpha(char)


__KEYWORDS: dict[str, TokenType] = {
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
        self.tokens = []

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _scan_token(self) -> None:
        c = self._advance()
        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
            case "/":
                if self._match("/"):
                    while (self._peek() != "\n") and (not self._is_at_end()):
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self._string()
            case c if isdigit(c):
                self._number()
            case c if is_alpha(c):
                self._identifier()
            case c:
                error.error(self.line, f"Unexpected character: {c}.")

        pass

    def _advance(self) -> str:
        current = self.current
        self.current += 1
        return self.source[current]

    def _add_token(self, type: TokenType, literal: object = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        elif not self.source[self.current:].startswith(expected):
            return False
        else:
            self.current += len(expected)
            return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\n"
        else:
            return self.source[self.current : self.current + 1]

    def _peek_next(self) -> str:
        if (self.current + 1) >= len(self.source):
            return "\n"
        return self.source[self.current + 1 : self.current + 2]

    def _string(self) -> None:
        while (self._peek() != '"') and (not self._is_at_end()):
            if self._peek() == '\n':
                self.line += 1
            self._advance()

        if self._is_at_end():
            error.error(self.line, "Unterminated string.")

        # consume `"`
        self._advance()

        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self) -> None:
        while isdigit(self._peek()):
            self._advance()

        if (self._peek() == ".") and (not isdigit(self._peek_next())):
            self._advance()
            while isdigit(self._peek()):
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def _identifier(self) -> None:
        while is_digit_or_alpha(self._peek()) or self._peek() == "_":
            self._advance()
        text = self.source[self.start : self.current]
        type = __KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add_token(type)
