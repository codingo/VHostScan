import unittest
from mock import Mock
from mock import patch

from lib.helpers.wordlist_helper import WordList
from lib.helpers.wordlist_helper import DEFAULT_WORDLIST_FILE


class TestWordList(unittest.TestCase):
    def setUp(self):
        self.wordlist = WordList()
        with open(DEFAULT_WORDLIST_FILE, 'r') as word_file:
            self.default_wordlist = list(word_file.read().splitlines())

    def test_get_wordlist_from_stdin(self):
        stdin_list = ['keyword1', 'keyword1']
        expected_wordlist = []
        expected_wordlist.extend(stdin_list)
        expected_wordlist.extend(self.default_wordlist)
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.read = Mock(return_value='\n'.join(stdin_list))
            mock_stdin.isatty = Mock(return_value=False)
            wordlist, wordlist_types = self.wordlist.get_wordlist()
            self.assertEqual(wordlist, expected_wordlist)

    def test_using_default_wordlist(self):
        wordlist, wordlist_types = self.wordlist.get_wordlist()
        self.assertEqual(wordlist, self.default_wordlist)
