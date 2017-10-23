import unittest
import pytest
from mock import patch

from lib.helpers.wordlist_helper import WordList
from lib.helpers.wordlist_helper import DEFAULT_WORDLIST_FILE


@pytest.fixture(scope='class')
def user_wordlist(request, tmpdir_factory):
    user_wordlist = ['user-word1', 'user-word2']
    tmpdir = tmpdir_factory.mktemp('user_wordlist')
    user_wordlist_file = tmpdir.join('user-wordlist.txt')
    user_wordlist_file.write('\n'.join(user_wordlist))
    request.cls.user_wordlist_file = str(user_wordlist_file)
    request.cls.user_wordlist = user_wordlist


@pytest.mark.usefixtures('user_wordlist')
class TestWordList(unittest.TestCase):
    def setUp(self):
        self.wordlist = WordList()
        with open(DEFAULT_WORDLIST_FILE, 'r') as word_file:
            self.default_wordlist = list(word_file.read().splitlines())

    def test_get_wordlist_from_stdin(self):
        stdin_wordlist = ['keyword1', 'keyword1']
        expected_wordlist = []
        expected_wordlist.extend(stdin_wordlist)
        with patch('lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist()
            self.assertEqual(wordlist, expected_wordlist)

    def test_get_wordlist_from_stdin_and_wordlist(self):
        stdin_wordlist = ['keyword1', 'keyword1']
        expected_wordlist = []
        expected_wordlist.extend(stdin_wordlist)
        expected_wordlist.extend(self.user_wordlist)
        with patch('lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(self.user_wordlist_file)
            self.assertEqual(wordlist, expected_wordlist)

    def test_using_default_wordlist(self):
        stdin_wordlist = []
        with patch('lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist()
            self.assertEqual(wordlist, self.default_wordlist)
