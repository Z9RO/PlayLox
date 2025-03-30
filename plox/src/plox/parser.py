from math import e
from plox import error
from plox.expr import BinaryExpr, Expr, GroupExpr, LiteralExpr, UnaryExpr
from plox.lox_token import Token, TokenType

class ParseException(Exception):
    pass

class parser:
    _tokens: list[Token]
    _current: int

    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._current = 0

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()
        while (
            type := self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)
        ) is not None:
            right = self._comparison()
            expr = BinaryExpr(type, expr, right)
        return expr

    def _comparison(self) -> Expr:
        expr = self._term()
        while (
            type := self._match(
                TokenType.LESS,
                TokenType.LESS_EQUAL,
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
            )
        ) is not None:
            right = self._comparison()
            expr = BinaryExpr(type, expr, right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while (type := self._match(TokenType.MINUS, TokenType.PLUS)) is not None:
            right = self._factor()
            expr = BinaryExpr(type, expr, right)
        return expr

    def _factor(self) -> Expr:
        expr = self._unary()
        while (type := self._match(TokenType.SLASH, TokenType.STAR)) is not None:
            right = self._unary()
            expr = BinaryExpr(type, expr, right)
        return expr

    def _unary(self) -> Expr:
        if (type := self._match(TokenType.BANG, TokenType.MINUS)) is not None:
            right = self._unary()
            return UnaryExpr(type, right)

        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.TRUE):
            return LiteralExpr(True)
        elif self._match(TokenType.FALSE):
            return LiteralExpr(False)
        elif self._match(TokenType.NIL):
            return LiteralExpr(None)
        elif self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self._previous().literal)
        
        if self._match(TokenType.LEFT_PAREN) is not None:
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupExpr(expr)
        
        raise self._error(self._peek(), "No match")

    def _match(self, *types: TokenType) -> TokenType | None:
        if self._is_at_end():
            return None
        type = next(filter(self._check, types), None)
        return type

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1

        return self._previous()

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]
    
    def _consume(self, type: TokenType, message: str) -> Token:
        if self._check(type):
            return self._advance()
        
        raise self._error(self._peek(), message)
    
    def _error(self, token: Token, message: str)-> ParseException:
        error.error(token.line, message)
        return ParseException()
