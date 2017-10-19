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
        return list(line for line in sys.stdin.read().splitlines()) \
            if not sys.stdin.isatty() else []

    def get_wordlist(self, wordlist_files=None):
        wordlist = []
        wordlist_types = []
        stdin_words = self.get_stdin_wordlist()
        if stdin_words:
            wordlist_types.append('stdin')
            wordlist.extend(stdin_words)
        combined_files = wordlist_files or DEFAULT_WORDLIST_FILE
        combined = get_combined_word_lists(combined_files)
        if combined:
            wordlist_types.append('wordlists: {}'.format(
                ', '.join(combined['file_paths'])))
            wordlist.extend(combined['words'])
        return wordlist, wordlist_types
