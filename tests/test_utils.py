import unittest

from src.utils import extract_title
from src.exceptions import ValueNotFoundError

class TestExtractTitle(unittest.TestCase):

    def setUp(self) -> None:
        self.file_path = "./tests/test_files/README.md"        
        self.empty_file = "./tests/test_files/empty.txt"
    def test_extract_h1(self):
        expected = "Static Site Generator"
        self.assertEqual(
            extract_title(self.file_path),
            expected
        )

    def test_raises_when_not_found(self):
        self.assertRaises(ValueNotFoundError, extract_title, self.empty_file)