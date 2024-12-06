import unittest
from whitespacetokenizer import whitespace_tokenizer


class TestWhitespaceTokenizer(unittest.TestCase):
    def test_tokenize_empty(self):
        self.assertEqual(whitespace_tokenizer(""), [])

    def test_tokenize_single(self):
        self.assertEqual(whitespace_tokenizer("hello"), [("hello", 0, 5)])

    def test_tokenize_multiple(self):
        self.assertEqual(whitespace_tokenizer("hello world"), [("hello", 0, 5), ("world", 6, 11)])

    def test_tokenize_multiple_spaces(self):
        self.assertEqual(whitespace_tokenizer("hello  world"), [("hello", 0, 5), ("world", 7, 12)])

    def test_tokenize_multiple_newlines(self):
        self.assertEqual(whitespace_tokenizer("hello\nworld"), [("hello", 0, 5), ("world", 6, 11)])

    def test_tokenize_multiple_tabs(self):
        self.assertEqual(whitespace_tokenizer("hello\tworld"), [("hello", 0, 5), ("world", 6, 11)])

    def test_tokenize_multiple_mixed(self):
        self.assertEqual(whitespace_tokenizer("hello \tworld"), [("hello", 0, 5), ("world", 7, 12)])

    def test_readme_case(self):
        self.assertEqual(
            whitespace_tokenizer("Hello, world! How are you?"),
            [("Hello,", 0, 6), ("world!", 7, 13), ("How", 14, 17), ("are", 18, 21), ("you?", 22, 26)]
        )