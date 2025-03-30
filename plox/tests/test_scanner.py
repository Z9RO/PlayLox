import unittest

from plox.scanner import Scanner, ScannerConfig
from plox.lox_token import Token, TokenType


class TestScanner(unittest.TestCase):
    def test_number(self):
        scanner = Scanner("233")
        result = scanner.scan_tokens()
        expected = [
            Token(TokenType.NUMBER, "233", 233, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        self.assertEqual(result, expected)

    def test_string(self):
        source = '''s = "multiple
        line"'''
        scanner = Scanner(source)
        result = scanner.scan_tokens()
        multiple_line = '''"multiple
        line"'''
        expected = [
            Token(TokenType.IDENTIFIER, "s", None, 1),
            Token(TokenType.EQUAL, "=", None, 1),
            Token(TokenType.STRING, multiple_line, None, 2),
            Token(TokenType.EOF, "", None, 2),
        ]
        self.assertEqual(result, expected)

    def test_comments(self):
        source = ''' is1 = a  == 1 // inline comments
        // all line are comments
        '''
        scanner = Scanner(source)
        result = scanner.scan_tokens()
        expected = [
            Token(TokenType.IDENTIFIER, 'is1', None, 1),
            Token(TokenType.EQUAL, '=', None, 1),
            Token(TokenType.IDENTIFIER, 'a', None, 1),
            Token(TokenType.EQUAL_EQUAL, '==', None, 1),
            Token(TokenType.NUMBER, '1', None, 1),
            Token(TokenType.EOF, '', None, 3),
        ]
        self.assertEqual(result, expected)

    def test_suit_0(self):
        source = """fun printSum(a, b) {
        print a + b;
        }"""
        scanner = Scanner(source)
        result = scanner.scan_tokens()
        expected = [
            Token(TokenType.FUN, "fun", None, 1),
            Token(TokenType.IDENTIFIER, "printSum", None, 1),
            Token(TokenType.LEFT_PAREN, "(", None, 1),
            Token(TokenType.IDENTIFIER, "a", None, 1),
            Token(TokenType.COMMA, ",", None, 1),
            Token(TokenType.IDENTIFIER, "b", None, 1),
            Token(TokenType.RIGHT_PAREN, ")", None, 1),
            Token(TokenType.LEFT_BRACE, "{", None, 1),
            Token(TokenType.PRINT, "print", None, 2),
            Token(TokenType.IDENTIFIER, "a", None, 2),
            Token(TokenType.PLUS, "+", None, 2),
            Token(TokenType.IDENTIFIER, "b", None, 2),
            Token(TokenType.SEMICOLON, ";", None, 2),
            Token(TokenType.RIGHT_BRACE, "}", None, 3),
            Token(TokenType.EOF, "", None, 3),
        ]
        self.assertEqual(result, expected)

    def test_single_comment(self):
        source = "1 // this is comment"
        config = ScannerConfig(True, False)
        scanner = Scanner(source, config)
        result = scanner.scan_tokens()
        expected = [
            Token(TokenType.NUMBER, "1", None, 1),
            Token(TokenType.SINGLELINECOMMENT, "// this is comment", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        self.assertEqual(result, expected)



if __name__ == "__main__":
    unittest.main()
