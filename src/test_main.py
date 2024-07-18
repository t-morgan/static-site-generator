import unittest

from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    
    def test_extract_title_strip_whitespace(self):
        self.assertEqual(extract_title("#   Hello Friends   "), "Hello Friends")


if __name__ == "__main__":
    unittest.main()