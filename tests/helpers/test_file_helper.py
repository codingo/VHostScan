import itertools
import pytest
import sys

from collections import namedtuple
from VHostScan.lib.helpers.file_helper import parse_word_list_argument, get_combined_word_lists, load_random_user_agents

WORDLIST_FILES = {
    'simpsons': ['marge', 'bart', 'homer', 'lisa', 'maggie'],
    'family_guy': ['stewie', 'lois', 'peter', 'brian', 'maggie', 'chris'],
    'flinstones': ['fred', 'bambam', 'wilma', 'barney', 'betty'],
    'duplicates': ['marge', 'bart'],
}

WordlistFiles = namedtuple('WordlistFiles', 'files words')

@pytest.fixture(scope='session')
def wordlist(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('wordlists')

    def create_file(filename):
        file = tmpdir.join(filename)
        file.write('\n'.join(WORDLIST_FILES[filename]))
        return str(file)

    words = list(itertools.chain.from_iterable(WORDLIST_FILES.values()))
    files = [create_file(file) for file in WORDLIST_FILES.keys()]

    return WordlistFiles(files=files, words=words)

def test_parse_word_list_argument(wordlist):
    argument = ','.join(wordlist.files + ['/non-existing-file'])
    result = parse_word_list_argument(argument)

    assert wordlist.files == result # non-existing files should be discarded

def test_get_combined_word_lists(wordlist):
    result = get_combined_word_lists(','.join(wordlist.files))

    assert wordlist.files == result['file_paths']
    assert wordlist.words == result['words']

def test_load_random_user_agents():
    expected = ['Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0']

    assert load_random_user_agents() == expected