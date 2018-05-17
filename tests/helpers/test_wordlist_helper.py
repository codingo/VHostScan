import unittest
import pytest
from unittest.mock import patch

from VHostScan.lib.helpers.wordlist_helper import WordList
from VHostScan.lib.helpers.wordlist_helper import DEFAULT_WORDLIST_FILE


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
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist()
            self.assertEqual(wordlist, expected_wordlist)

    def test_get_wordlist_from_stdin_and_wordlist(self):
        stdin_wordlist = ['keyword1', 'keyword1']
        expected_wordlist = []
        expected_wordlist.extend(stdin_wordlist)
        expected_wordlist.extend(self.user_wordlist)
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(self.user_wordlist_file)
            self.assertEqual(wordlist, expected_wordlist)

    def test_using_default_wordlist(self):
        stdin_wordlist = []
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist()
            self.assertEqual(wordlist, self.default_wordlist)

    def test_ip_using_prefix(self):
        stdin_wordlist = ['127.0.0.1']
        prefix = 'dev-'
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(None, prefix)
            self.assertEqual(wordlist, stdin_wordlist)

    def test_ip_using_suffix(self):
        stdin_wordlist = ['127.0.0.1']
        suffix = 'test'
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(None,None,suffix)
            self.assertEqual(wordlist,stdin_wordlist)

    def test_ipv6_using_prefix(self):
        stdin_wordlist = ['::1']
        prefix = 'dev-'
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(None, prefix)
            self.assertEqual(wordlist, stdin_wordlist)

    def test_ipv6_using_suffix(self):
        stdin_wordlist = ['::1']
        suffix = 'test'
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(None,None,suffix)
            self.assertEqual(wordlist,stdin_wordlist)

    def test_word_with_prefix(self):
        stdin_wordlist = ['www','www2','www3']
        expected_wordlist = stdin_wordlist + ['dev-www','dev-www2','dev-www3']
        prefix = 'dev-'
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types =  self.wordlist.get_wordlist(None,prefix)
            self.assertEqual(wordlist,expected_wordlist)

    def test_words_with_suffix(self):
        stdin_wordlist = ['www','www2','www3']
        expected_wordlist = stdin_wordlist + ['wwwtest','www2test','www3test']
        suffix = 'test'
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(None,None,suffix)
            self.assertEqual(wordlist, expected_wordlist)

    def test_words_with_host_and_prefix(self):
        stdin_wordlist = ['www.%s']
        expected_wordlist = stdin_wordlist + ['test-www.%s']
        prefix = 'test-'
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(None, prefix)
            self.assertEqual(wordlist, expected_wordlist)

    def test_words_with_host_and_suffix(self):
        stdin_wordlist = ['www.%s']
        expected_wordlist = stdin_wordlist + ['wwwtest.%s']
        suffix = 'test'
        with patch('VHostScan.lib.helpers.wordlist_helper.WordList.get_stdin_wordlist', return_value=stdin_wordlist):
            wordlist, wordlist_types = self.wordlist.get_wordlist(None,None,suffix)
            self.assertEqual(wordlist, expected_wordlist)




