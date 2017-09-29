import os


class file_helper(object):
    """description of class"""
    def __init__(self, output_file):
        self.output_file = output_file

    def check_directory(self):
        directory = self.output_file
        try:
            os.stat(self.directory)
        except:
            os.mkdir(self.directory)
            print("[!] %s didn't exist and has been created." % output_directory)

    # placeholder for error checking on -oJ implementation
    def is_json(json_file):
        try:
            with open(json_file, "r") as f: 
                json_object = json.load(f)
        except ValueError:
            return False
        return True

    def write_file(self, contents):
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
