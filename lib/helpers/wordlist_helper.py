import sys


class WordList:
    def get_stdin_wordlist(self):
        return list(line for line in sys.stdin.read().splitlines()) if not sys.stdin.isatty() else []
