import pytest

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

@pytest.fixture()
def wordlist():
    wordlist = WordList()
    return wordlist

@pytest.fixture(scope="module")
def default_wordlist():
    wordlist = []
    with open(DEFAULT_WORDLIST_FILE, 'r') as word_file:
        wordlist = list(word_file.read().splitlines())
    return wordlist

@pytest.mark.usefixtures('user_wordlist')
class TestWordList(object):

    def test_get_wordlist_from_stdin(self, monkeypatch, wordlist):
        print(dir(TestWordList))
        stdin_wordlist = ['keyword1', 'keyword1']
        expected_wordlist = []
        expected_wordlist.extend(stdin_wordlist)
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist()
        assert wordlist_result == expected_wordlist

    def test_get_wordlist_from_stdin_and_wordlist(self, monkeypatch, wordlist):
        stdin_wordlist = ['keyword1', 'keyword1']
        expected_wordlist = []
        expected_wordlist.extend(stdin_wordlist)
        expected_wordlist.extend(self.user_wordlist)
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist(self.user_wordlist_file)
        assert wordlist_result == expected_wordlist

    def test_using_default_wordlist(self, monkeypatch, wordlist, default_wordlist):
        stdin_wordlist = []
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist()
        assert wordlist_result == default_wordlist

    def test_ip_using_prefix(self, monkeypatch, wordlist):
        stdin_wordlist = ['127.0.0.1']
        prefix = 'dev-'
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist(None, prefix)
        assert wordlist_result == stdin_wordlist

    def test_ip_using_suffix(self, monkeypatch, wordlist):
        stdin_wordlist = ['127.0.0.1']
        suffix = 'test'
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist(None,None,suffix)
        assert wordlist_result == stdin_wordlist

    def test_ipv6_using_prefix(self, monkeypatch, wordlist):
        stdin_wordlist = ['::1']
        prefix = 'dev-'
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist(None, prefix)
        assert wordlist_result == stdin_wordlist

    def test_ipv6_using_suffix(self, monkeypatch, wordlist):
        stdin_wordlist = ['::1']
        suffix = 'test'
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist(None,None,suffix)
        assert wordlist_result == stdin_wordlist

    def test_word_with_prefix(self, monkeypatch, wordlist):
        stdin_wordlist = ['www','www2','www3']
        expected_wordlist = stdin_wordlist + ['dev-www','dev-www2','dev-www3']
        prefix = 'dev-'
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types =  wordlist.get_wordlist(None,prefix)
        assert wordlist_result == expected_wordlist

    def test_words_with_suffix(self, monkeypatch, wordlist):
        stdin_wordlist = ['www','www2','www3']
        expected_wordlist = stdin_wordlist + ['wwwtest','www2test','www3test']
        suffix = 'test'
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist(None,None,suffix)
        assert wordlist_result == expected_wordlist

    def test_words_with_host_and_prefix(self, monkeypatch, wordlist):
        stdin_wordlist = ['www.%s']
        expected_wordlist = stdin_wordlist + ['test-www.%s']
        prefix = 'test-'
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist(None, prefix)
        assert wordlist_result == expected_wordlist

    def test_words_with_host_and_suffix(self, monkeypatch, wordlist):
        stdin_wordlist = ['www.%s']
        expected_wordlist = stdin_wordlist + ['wwwtest.%s']
        suffix = 'test'
        monkeypatch.setattr(WordList, 'get_stdin_wordlist', (lambda x: stdin_wordlist))
        wordlist_result, wordlist_types = wordlist.get_wordlist(None,None,suffix)
        assert wordlist_result == expected_wordlist




