import sys
from ipaddress import ip_address, AddressValueError
from typing import List, Tuple, Union, Optional

from pkg_resources import resource_filename

from .file_helper import get_combined_word_lists

DEFAULT_WORDLIST_FILE = resource_filename(
    'VHostScan', 'wordlists/virtual-host-scanning.txt')


class WordList:
    def __init__(self):
        self.wordlist: List[str] = []
        self.wordlist_types: List[str] = []

    def get_stdin_wordlist(self) -> List[str]:
        """Get wordlist from stdin if available"""
        return list(line for line in sys.stdin.read().splitlines()) \
            if not sys.stdin.isatty() else []

    def get_wordlist(self,
                     wordlist_files: Optional[str] = None,
                     wordlist_prefix: Union[str, bool] = False,
                     wordlist_suffix: Union[str, bool] = False) -> Tuple[List[str], List[str]]:
        """Get combined wordlist from various sources"""

        default_wordlist_file = DEFAULT_WORDLIST_FILE

        stdin_words = self.get_stdin_wordlist()
        if stdin_words:
            self.set_words(words_type='stdin', words=stdin_words)
            default_wordlist_file = None

        combined_files = wordlist_files or default_wordlist_file
        if combined_files:
            combined = get_combined_word_lists(combined_files)
        else:
            combined = None

        if combined:
            words_type = 'wordlists: {}'.format(
                ', '.join(combined['file_paths']))
            self.set_words(words_type=words_type, words=combined['words'])

        # Apply prefixes
        if wordlist_prefix:
            prefixed = []
            for word in self.wordlist:
                if word == '%s':
                    continue
                elif self.valid_ip(word):
                    continue
                else:
                    prefixed.append(str(wordlist_prefix) + word)

            if len(prefixed) > 0:
                self.wordlist = self.wordlist + prefixed

        if wordlist_suffix:
            suffixed = []
            for word in self.wordlist:
                if word == '%s':
                    continue
                elif self.valid_ip(word):
                    continue
                elif ".%s" in word:
                    split = word.split(".")
                    suffixed.append(split[0] + str(wordlist_suffix) + ".%s")
                else:
                    suffixed.append(word + str(wordlist_suffix))

            if len(suffixed) > 0:
                self.wordlist = self.wordlist + suffixed

        return self.wordlist, self.wordlist_types

    def set_words(self, words_type: str, words: List[str]) -> None:
        """Add words to wordlist with type tracking"""
        self.wordlist_types.append(words_type)
        self.wordlist.extend(words)

    def valid_ip(self, address: str) -> bool:
        """Check if address is a valid IP"""
        try:
            return ip_address(address) is not None
        except (AddressValueError, ValueError):
            return False
