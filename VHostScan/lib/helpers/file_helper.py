import json
import os

from pkg_resources import resource_filename

DEFAULT_UA_LIST = resource_filename(
    'VHostScan', 'lib/ua-random-list.txt')


class file_helper(object):
    """description of class"""
    def __init__(self, output_file):
        self.output_file = output_file

    def check_directory(self):
        directory = os.path.dirname(self.output_file)

        if directory != '':
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)
                print("[!] {} didn't exist and has been created.".format(
                    directory))

    def is_json(json_file):
        try:
            with open(json_file, "r") as f:
                json_object = json.load(f)
        except ValueError:
            return False
        return True

    def write_file(self, contents):
        # check if host directory exists, if not create it
        self.check_directory()

        with open(self.output_file, "w") as o:
            o.write(contents)


def parse_word_list_argument(argument):
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


def get_combined_word_lists(argument):
    files = parse_word_list_argument(argument)
    words = []

    for path in files:
        with open(path) as f:
            words.extend(f.read().splitlines())

    return {
        'file_paths': files,
        'words': words,
    }


def load_random_user_agents():
    with open(DEFAULT_UA_LIST) as f:
        return f.read().splitlines()
