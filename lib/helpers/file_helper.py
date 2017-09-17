import os


class file_helper(object):
    """description of class"""
    def __init__(self, output_file):
        self.output_file = output_file

    def check_directory(output_directory):
        try:
            os.stat(output_directory)
        except:
            os.mkdir(output_directory)
            print("[!] %s didn't exist and has been created." % output_directory)

    # validate json of output
    def is_json(json_file):
        try:
            with open(json_file, "r") as f: 
                json_object = json.load(f)
        except ValueError:
            return False
        return True        