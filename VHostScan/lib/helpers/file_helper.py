import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from pkg_resources import resource_filename

DEFAULT_UA_LIST = resource_filename(
    'VHostScan', 'lib/ua-random-list.txt')


class file_helper(object):
    """File helper for output operations"""
    def __init__(self, output_file: str):
        self.output_file = output_file

    def check_directory(self) -> None:
        """Create directory if it doesn't exist"""
        directory = os.path.dirname(self.output_file)

        if directory != '':
            Path(directory).mkdir(parents=True, exist_ok=True)
            if not os.path.exists(directory):
                print(f"[!] {directory} didn't exist and has been created.")

    def write_file(self, contents: str) -> None:
        """Write contents to file with proper encoding"""
        # check if host directory exists, if not create it
        self.check_directory()

        with open(self.output_file, "w", encoding='utf-8') as o:
            o.write(contents)


def parse_word_list_argument(argument: Optional[str]) -> List[str]:
    """Parse wordlist argument and return list of valid file paths"""
    if not argument:
        return []

    if ',' in argument:
        files = [arg.strip() for arg in argument.split(',')]
    else:
        files = [argument.strip()]

    return [
        path for path in files
        if os.path.exists(path)
    ]


def get_combined_word_lists(argument: Optional[str]) -> Dict[str, Any]:
    """Get combined wordlists from files"""
    if not argument:
        return {'file_paths': [], 'words': []}
        
    files = parse_word_list_argument(argument)
    words = []

    for path in files:
        with open(path, encoding='utf-8') as f:
            words.extend(f.read().splitlines())

    return {
        'file_paths': files,
        'words': words,
    }


def load_random_user_agents() -> List[str]:
    """Load random user agents from file"""
    with open(DEFAULT_UA_LIST, encoding='utf-8') as f:
        return f.read().splitlines()
