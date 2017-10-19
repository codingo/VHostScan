import sys
import os
from lib.helpers.file_helper import get_combined_word_lists

DEFAULT_WORDLIST_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../..',
    'wordlists',
    'virtual-host-scanning.txt'
)


class WordList:
    def get_stdin_wordlist(self):
        return list(line for line in sys.stdin.read().splitlines()) if not sys.stdin.isatty() else []

    def get_wordlist(self, wordlist_files=None):
        wordlist = []
        stdin_words = self.get_stdin_wordlist()
        if stdin_words:
            wordlist.extend(stdin_words)
        combined = get_combined_word_lists(wordlist_files or DEFAULT_WORDLIST_FILE)
        wordlist.extend(combined['words'])
        return wordlist
