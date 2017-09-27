from lib.core.discovered_host import *
from lib.helpers.file_helper import *
import time
from fuzzywuzzy import fuzz
import itertools
import numpy as np


class output_helper(object):
    def __init__(self, scanner):
        self.scanner = scanner

    def write_normal(self, filename):
        
        file = file_helper(filename)

        # todo: finish check_directory (needs regex to split out filename)
        # file.check_directory(filename)
        file.write_file(self.generate_header() + self.output_normal_likely() + self.output_fuzzy() + self.output_normal_detail())

    def output_normal_likely(self):
        uniques = False
        depth = str(self.scanner.unique_depth)
        output = "\n[+] Most likely matches with a unique count of {} or less:".format(depth)
        
        for p in self.scanner.likely_matches(): 
            output += "\n\t[>] {}".format(p)
            uniques = True
        
        if(uniques):
            return output
        else:
            return "\n[!] No matches with a unique count of {} or less.".format(depth)


    def output_fuzzy(self):
        output = "\n[+] Match similarity using fuzzy logic:"
        request_hashes = {}
        
        for host in self.scanner.hosts:
            request_hashes[host.hash] = host.content
        
        for a, b in itertools.combinations(request_hashes.keys(), 2):
            output += "\n\t[>] {} is {}% similar to {}".format(a, fuzz.ratio(request_hashes[a], request_hashes[b]), b)
        
        return output


    def output_normal_detail(self):
        output = "\n\n[+] Full scan results"

        for host in self.scanner.hosts: 
            output += "\n\n{} (Code: {}) hash: {}".format(str(host.hostname), str(host.response_code), str(host.hash))
            for key in host.keys: output += "\n\t{}".format(key)
        
        return output


    def generate_header(self):
        output = "VHostScanner Log: {} {}\n".format(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
        output += "\tTarget: {}\n\tBase Host: {}\n\tPort: {}".format(self.scanner.target, self.scanner.base_host, self.scanner.port)
        output += "\n\tReal Port {}\n\tIgnore HTTP Codes: {}".format(self.scanner.real_port,self.scanner.ignore_http_codes)
        output += "\n\tIgnore Content Length: {}\n\tWordlist: {}".format(self.scanner.ignore_content_length, self.scanner.wordlist)
        output += "\n\tUnique Depth: {}\n\tSSL: {}\n\t".format(self.scanner.unique_depth, self.scanner.ssl)
        return output
