import os
import requests
import hashlib
import pandas as pd
from lib.core.discovered_host import *
from fuzzywuzzy import fuzz


class virtual_host_scanner(object):
    """Virtual host scanning class
    
    Virtual host scanner has the following properties:
    
    Attributes:
        wordlist: location to a wordlist file to use with scans
        target: the target for scanning
        port: the port to scan. Defaults to 80
        ignore_http_codes: commad seperated list of http codes to ignore
        ignore_content_length: integer value of content length to ignore
        output: folder to write output file to
    """
     
    def __init__(self, target, base_host, wordlist, port=80, real_port=80, ssl=False, unique_depth=1, ignore_http_codes='404', ignore_content_length=0, fuzzy_logic=False, add_waf_bypass_headers=False):
        self.target = target
        self.base_host = base_host
        self.port = int(port)
        self.real_port = int(real_port)
        self.ignore_http_codes = list(map(int, ignore_http_codes.replace(' ', '').split(',')))
        self.ignore_content_length = ignore_content_length
        self.wordlist = wordlist
        self.unique_depth = unique_depth
        self.ssl = ssl
        self.fuzzy_logic = fuzzy_logic
        self.add_waf_bypass_headers = add_waf_bypass_headers

        # this can be made redundant in future with better exceptions
        self.completed_scan=False
        
        # this is maintained until likely-matches is refactored to use new class
        self.results = []
        
        # store associated data for discovered hosts in array for oN, oJ, etc'
        self.hosts = []


    def scan(self):
        if not self.base_host:
            self.base_host = self.target

        if not self.real_port:
            self.real_port = self.port

        for virtual_host in self.wordlist:
            hostname = virtual_host.replace('%s', self.base_host)

            if self.add_waf_bypass_headers:
                headers = {
                    'Host': hostname if self.real_port == 80 else '{}:{}'.format(hostname, self.real_port),
                    'Accept': '*/*',
                    'X-Originating-IP': '127.0.0.1',
                    'X-Forwarded-For': '127.0.0.1',
                    'X-Remote-IP': '127.0.0.1',
                    'X-Remote-Addr': '127.0.0.1'
                }
            else:
                headers = {
                    'Host': hostname if self.real_port == 80 else '{}:{}'.format(hostname, self.real_port),
                    'Accept': '*/*'
                }
            
            dest_url = '{}://{}:{}/'.format('https' if self.ssl else 'http', self.target, self.port)

            try:
                res = requests.get(dest_url, headers=headers, verify=False)
            except requests.exceptions.RequestException:
                continue

            if res.status_code in self.ignore_http_codes:
                continue

            if self.ignore_content_length > 0 and self.ignore_content_length == int(res.headers.get('content-length')):
                continue

            # hash the page results to aid in identifing unique content
            page_hash = hashlib.sha256(res.text.encode('utf-8')).hexdigest()
            output = '[#] Found: {} (code: {}, length: {}, hash: {})\n'.format(hostname, res.status_code, 
                                                                               res.headers.get('content-length'), page_hash)
            host = discovered_host()
            host.hostname = hostname
            host.response_code = res.status_code
            host.hash = page_hash
            host.content = res.content

            for key, val in res.headers.items():
                output += '  {}: {}\n'.format(key, val)
                host.keys.append('{}: {}'.format(key, val))

            self.hosts.append(host)
            
            # print current results so feedback remains in "realtime"
            print(output)

            # add url and hash into array for likely matches
            self.results.append(hostname + ',' + page_hash)

        self.completed_scan=True


    def likely_matches(self):
        if self.completed_scan is False:
            print("[!] Likely matches cannot be printed as a scan has not yet been run.")
            return      

        # segment results from previous scan into usable results
        segmented_data={}
        for item in self.results:
            result = item.split(",")
            segmented_data[result[0]] = result[1]

        dataframe = pd.DataFrame([[key, value] for key, value in segmented_data.items()], columns=["key_col", "val_col"])
        segmented_data = dataframe.groupby("val_col").filter(lambda x: len(x) <= self.unique_depth)
        matches = ((segmented_data["key_col"].values).tolist())

        return matches

    def fuzzy_logic(self):
       # for host in self.hosts:
       return