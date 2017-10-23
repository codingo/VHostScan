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
    def __init__(self):
        self.wordlist = []
        self.wordlist_types = []

    def get_stdin_wordlist(self):
        return list(line for line in sys.stdin.read().splitlines()) \
            if not sys.stdin.isatty() else []

    def get_wordlist(self, wordlist_files=None):
        default_wordlist_file = DEFAULT_WORDLIST_FILE

        stdin_words = self.get_stdin_wordlist()
        if stdin_words:
            self.set_words(words_type='stdin', words=stdin_words)
            default_wordlist_file = None

        combined_files = wordlist_files or default_wordlist_file
        combined = get_combined_word_lists(combined_files)
        if combined:
            words_type = 'wordlists: {}'.format(
                ', '.join(combined['file_paths']))
            self.set_words(words_type=words_type, words=combined['words'])

        return self.wordlist, self.wordlist_types

    def set_words(self, words_type, words):
        self.wordlist_types.append(words_type)
        self.wordlist.extend(words)
