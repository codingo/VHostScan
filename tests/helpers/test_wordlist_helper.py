import unittest
from mock import Mock
from mock import patch

from lib.helpers.wordlist_helper import WordList


class TestWordList(unittest.TestCase):
    def setUp(self):
        self.wordlist = WordList()

    def test_get_wordlist_from_stdin(self):
        stdin_list = ['keyword1', 'keyword1']
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.read = Mock(return_value='\n'.join(stdin_list))
            mock_stdin.isatty = Mock(return_value=False)
            self.assertEqual(self.wordlist.get_stdin_wordlist(), stdin_list)
