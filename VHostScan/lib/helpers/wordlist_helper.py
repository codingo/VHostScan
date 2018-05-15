import sys
from .file_helper import get_combined_word_lists
from pkg_resources import resource_filename
from ipaddress import ip_address

DEFAULT_WORDLIST_FILE = resource_filename(
    'VHostScan', 'wordlists/virtual-host-scanning.txt')


class WordList:
    def __init__(self):
        self.wordlist = []
        self.wordlist_types = []

    def get_stdin_wordlist(self):
        return list(line for line in sys.stdin.read().splitlines()) \
            if not sys.stdin.isatty() else []

    def get_wordlist(self,
                     wordlist_files=None,
                     wordlist_prefix=False,
                     wordlist_suffix=False):

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

        # Apply prefixes
        if wordlist_prefix:
            prefixed = []
            for word in self.wordlist:
                if(word == '%s'):
                    continue
                elif(self.valid_ip(word)):
                    continue
                else:
                    prefixed.append(wordlist_prefix + word)

            if len(prefixed) > 0:
                self.wordlist = self.wordlist + prefixed

        if wordlist_suffix:
            suffixed = []
            for word in self.wordlist:
                if(word == '%s'):
                    continue
                elif(self.valid_ip(word)):
                    continue
                elif(".%s" in word):
                    split = word.split(".")
                    suffixed.append(split[0] + wordlist_suffix + ".%s")
                else:
                    suffixed.append(word + wordlist_suffix)

            if len(suffixed) > 0:
                self.wordlist = self.wordlist + suffixed

        return self.wordlist, self.wordlist_types

    def set_words(self, words_type, words):
        self.wordlist_types.append(words_type)
        self.wordlist.extend(words)

    def valid_ip(self, address):
        try:
            return ip_address(address) is not None
        except:
            return False
