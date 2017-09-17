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