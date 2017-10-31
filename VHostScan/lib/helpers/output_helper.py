from ..core.discovered_host import *
from .file_helper import *
import time
from fuzzywuzzy import fuzz
import itertools
import numpy as np
import json


class output_helper(object):
    def __init__(self, scanner, arguments):
        self.scanner = scanner
        self.arguments = arguments

    def write_normal(self, filename):
        file = file_helper(filename)

        output = self.generate_header()
        output += self.output_normal_likely()

        if(self.arguments.fuzzy_logic):
            output += self.output_fuzzy()

        output += self.output_normal_detail()
        file.write_file(output)

    def write_grepable(self, filename):
        file = file_helper(filename)

        output = self.generate_header()
        output += self.output_grepable_detail()

        file.write_file(output)

    def output_normal_likely(self):
        uniques = False
        depth = str(self.scanner.unique_depth)
        output = (
            "\n[+] Most likely matches with a unique count "
            "of {} or less:").format(depth)

        for p in self.scanner.likely_matches():
            output += "\n\t[>] {}".format(p)
            uniques = True

        if(uniques):
            return output
        else:
            return (
                "\n[!] No matches with an"
                " unique count of {} or less.").format(depth)

    def output_json(self, filename):
        file = file_helper(filename)
        output = dict()
        output['Target'] = self.scanner.target
        output['Base Host'] = self.scanner.base_host
        output['Port'] = self.scanner.port
        output['Real Port'] = self.scanner.real_port
        output['Ignore HTTP Codes'] = self.scanner.ignore_http_codes
        output['Ignore Content Length'] = self.scanner.ignore_content_length
        output['Wordlist'] = self.scanner.wordlist
        output['Unique Depth'] = self.scanner.unique_depth
        output['SSL'] = self.scanner.ssl
        output['Start Time'] = '{} {}'.format(
            time.strftime("%d/%m/%Y"),
            time.strftime("%H:%M:%S")
        )

        result = dict()
        for host in self.scanner.hosts:
            headers = dict()
            for header in host.keys:
                headers[header.split(':')[0]] = header.split(':')[1].strip()

            result[host.hostname] = {
                'Code': host.response_code,
                'Hash': host.hash,
                'Headers': headers
            }

        output['Result'] = result

        if not file.is_json(output):
            print("[!] Json format check failed")

        file.write_file(json.dumps(output, indent=2))

    def output_fuzzy(self):
        output = "\n\n[+] Match similarity using fuzzy logic:"
        request_hashes = {}

        for host in self.scanner.hosts:
            request_hashes[host.hash] = host.content

        for a, b in itertools.combinations(request_hashes.keys(), 2):
            output += "\n\t[>] {} is {}% similar to {}".format(
                a,
                fuzz.ratio(request_hashes[a], request_hashes[b]),
                b
            )

        return output

    def output_normal_detail(self):
        output = "\n\n[+] Full scan results"

        for host in self.scanner.hosts:
            output += "\n\n{} (Code: {}) hash: {}".format(
                str(host.hostname),
                str(host.response_code),
                str(host.hash)
            )

            for key in host.keys:
                output += "\n\t{}".format(key)

        return output

    def output_grepable_detail(self):
        for host in self.scanner.hosts:
            output += "\n{}\t{}\t{}".format(
                str(host.hostname),
                str(host.response_code),
                str(host.hash)
            )

        return output

    def generate_header(self):
        output = "VHostScanner Log: {} {}\n".format(
            time.strftime("%d/%m/%Y"),
            time.strftime("%H:%M:%S")
        )

        output += "\tTarget: {}\n\tBase Host: {}\n\tPort: {}".format(
            self.scanner.target,
            self.scanner.base_host,
            self.scanner.port
        )

        output += "\n\tReal Port {}\n\tIgnore HTTP Codes: {}".format(
            self.scanner.real_port,
            self.scanner.ignore_http_codes
        )

        output += "\n\tIgnore Content Length: {}\n\tWordlist: {}".format(
            self.scanner.ignore_content_length,
            self.scanner.wordlist
        )

        output += "\n\tUnique Depth: {}\n\tSSL: {}\n\t".format(
            self.scanner.unique_depth,
            self.scanner.ssl
        )

        return output
