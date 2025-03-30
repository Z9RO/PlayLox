from dataclasses import dataclass
from typing import Protocol

from plox.lox_token import Token, TokenType


class Expr:
    def accept[T](self, visitor: "ExprVisitor[T]"): ...


@dataclass
class BinaryExpr(Expr):
    operator: TokenType
    left: Expr
    right: Expr

    def accept(self, visitor):
        return visitor.visit_binary(self)


@dataclass
class UnaryExpr(Expr):
    operator: TokenType
    right: Expr

    def accept(self, visitor):
        return visitor.visit_unary(self)


@dataclass
class GroupExpr(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visit_group(self)


@dataclass
class LiteralExpr(Expr):
    value: object | None

    def accept(self, visitor):
        return visitor.visit_literal(self)


class ExprVisitor[T](Protocol):

    def visit_binary(self, expr: BinaryExpr) -> T: ...

    def visit_unary(self, expr: UnaryExpr) -> T: ...

    def visit_group(self, expr: GroupExpr) -> T: ...

    def visit_literal(self, expr: LiteralExpr) -> T: ...
