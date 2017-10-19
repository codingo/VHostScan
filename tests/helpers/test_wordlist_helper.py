import unittest
from mock import patch

from lib.helpers.wordlist_helper import WordList
from lib.helpers.wordlist_helper import DEFAULT_WORDLIST_FILE


class TestWordList(unittest.TestCase):
    def setUp(self):
        self.wordlist = WordList()
        with open(DEFAULT_WORDLIST_FILE, 'r') as word_file:
            self.default_wordlist = list(word_file.read().splitlines())

    def test_get_wordlist_from_stdin(self):
        stdin_wordlist = ['keyword1', 'keyword1']
        expected_wordlist = []
        expected_wordlist.extend(stdin_wordlist)
        expected_wordlist.extend(self.default_wordlist)
        with patch('lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist()
            self.assertEqual(wordlist, expected_wordlist)

    def test_using_default_wordlist(self):
        stdin_wordlist = []
        with patch('lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist()
            self.assertEqual(wordlist, self.default_wordlist)
