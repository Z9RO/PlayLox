from curses.ascii import isalpha, isdigit
from dataclasses import dataclass
from plox import error
from plox.lox_token import Token, TokenType


def is_alpha(char: str) -> bool:
    return isalpha(char) or char == "_"


def is_digit_or_alpha(char: str) -> bool:
    return isdigit(char) or is_alpha(char)


_KEYWORDS: dict[str, TokenType] = {
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

_SINGLE_CHAR_TOKENS: dict[str, TokenType] = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    ";": TokenType.SEMICOLON,
    "*": TokenType.STAR,
}

_DOUBLE_CHAR_TOKENS = {
    "!": (TokenType.BANG_EQUAL, TokenType.BANG),
    "=": (TokenType.EQUAL_EQUAL, TokenType.EQUAL),
    "<": (TokenType.LESS_EQUAL, TokenType.LESS),
    ">": (TokenType.GREATER_EQUAL, TokenType.GREATER),
}


@dataclass
class ScannerConfig:
    comment_as_token: bool = False
    multi_line_comments: bool = False
    nest_comments: bool = False


class Scanner:
    _source: str
    _tokens: list[Token]
    _start: int
    _current: int
    _line: int
    _config: ScannerConfig

    def __init__(self, source: str, config: ScannerConfig | None = None):
        self._source = source
        self._start = 0
        self._current = 0
        self._line = 1
        self._tokens = []
        self._config = config if config is not None else ScannerConfig()

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def _scan_token(self) -> None:
        c = self._advance()
        if token_type := _SINGLE_CHAR_TOKENS.get(c):
            self._add_token(token_type)
        elif token_types := _DOUBLE_CHAR_TOKENS.get(c):
            [double, single] = token_types
            token_type = double if self._match("=") else single
            self._add_token(token_type)
        elif c == "/":
            if self._match("/"):
                while (self._peek() != "\n") and (not self._is_at_end()):
                    self._advance()
                if self._config.comment_as_token:
                    comment = self._source[self._start + 2 : self._current]
                    self._add_token(TokenType.SINGLELINECOMMENT, comment)
            elif self._config.multi_line_comments and self._match("*"):
                if self._config.nest_comments:
                    self._nest_multiple_line_comments()
                else:
                    self._multiple_line_comments()
            else:
                self._add_token(TokenType.SLASH)
        elif c in "\r \t":
            # ignore whitespace
            pass
        elif c == "\n":
            self._line += 1
        elif c == '"':
            self._string()
        elif isdigit(c):
            self._number()
        elif is_alpha(c):
            self._identifier()
        else:
            error.error(self._line, f"Unexpected character: {c}.")

        pass

    def _advance(self) -> str:
        char = self._source[self._current]
        self._current += 1
        return char

    def _add_token(self, type: TokenType, literal: object = None) -> None:
        text = self._source[self._start : self._current]
        self._tokens.append(Token(type, text, literal, self._line))

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        elif not self._source[self._current :].startswith(expected):
            return False
        else:
            self._current += len(expected)
            return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\n"
        else:
            return self._source[self._current]

    def _peek_next(self) -> str:
        if (self._current + 1) >= len(self._source):
            return "\n"
        return self._source[self._current + 1]

    def _string(self) -> None:
        while (self._peek() != '"') and (not self._is_at_end()):
            if self._peek() == "\n":
                self._line += 1
            self._advance()

        if self._is_at_end():
            error.error(self._line, "Unterminated string.")

        # consume `"`
        self._advance()

        value = self._source[self._start + 1 : self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self) -> None:
        while isdigit(self._peek()):
            self._advance()

        if (self._peek() == ".") and (not isdigit(self._peek_next())):
            self._advance()
            while isdigit(self._peek()):
                self._advance()

        self._add_token(
            TokenType.NUMBER, float(self._source[self._start : self._current])
        )

    def _identifier(self) -> None:
        while is_digit_or_alpha(self._peek()) or self._peek() == "_":
            self._advance()
        text = self._source[self._start : self._current]
        type = _KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add_token(type)

    def _multiple_line_comments(self) -> None:
        while not self._is_at_end():
            if self._match("\n"):
                self._line+=1
            elif self._match("*/"):
                if self._config.comment_as_token:
                    comment = self._source[self._start + 2 : self._current - 2]
                    self._add_token(TokenType.MULTILINECOMMENT, comment)
                return
            else:
                self._advance()

        error.error(self._line, "Unterminated multiple line comments")

    def _nest_multiple_line_comments(self) -> None:
        level = 1
        while not self._is_at_end():
            if self._match("\n"):
                self._line += 1
            elif self._match("*/"):
                level -= 1
                if level == 0:
                    if self._config.comment_as_token:
                        comment = self._source[self._start + 2 : self._current - 2]
                        self._add_token(TokenType.MULTILINECOMMENT, comment)
                    return
            elif self._match("/*"):
                level += 1
            else:
                self._advance()
        pass
        error.error(self._line, "Unterminated multiple line comments")
