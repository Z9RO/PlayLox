import unittest

from plox.expr import BinaryExpr, Expr, LiteralExpr
from plox.lox_token import TokenType
from plox.parser import Parser
from plox.scanner import Scanner

def _build_Expr(source: str) -> Expr | None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    return parser.parse()

class TestParser(unittest.TestCase):
    def test_suit_0(self):
        code = "5 == 1"
        expr = _build_Expr(code)
        expected = BinaryExpr(TokenType.EQUAL_EQUAL, LiteralExpr(5), LiteralExpr(1))
        self.assertEqual(expr, expected)

    def test_suit_1(self):
        code = "90 + 8 *3"
        expr = _build_Expr(code)
        expected = BinaryExpr(TokenType.PLUS, LiteralExpr(90), BinaryExpr(TokenType.STAR, LiteralExpr(8), LiteralExpr(3)))
        self.assertEqual(expr, expected)
