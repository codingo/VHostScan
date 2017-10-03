import os
import requests
import hashlib
import pandas as pd
import time
from lib.core.discovered_host import *


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


    def __init__(self, target, wordlist, **kwargs):
        self.target = target
        self.wordlist = wordlist
        self.base_host = kwargs.get('base_host')
        self.rate_limit = int(kwargs.get('rate_limit', 0))
        self.port = int(kwargs.get('port', 80))
        self.real_port = int(kwargs.get('real_port', 80))
        self.ignore_content_length = int(kwargs.get('ignore_content_length', 0))
        self.ssl = kwargs.get('ssl', False)
        self.fuzzy_logic = kwargs.get('fuzzy_logic', False)
        self.add_waf_bypass_headers = kwargs.get('add_waf_bypass_headers', False)
        self.unique_depth = int(kwargs.get('unique_depth', 1))
        self.ignore_http_codes = kwargs.get('ignore_http_codes', '404')

        # this can be made redundant in future with better exceptions
        self.completed_scan=False
        
        # this is maintained until likely-matches is refactored to use new class
        self.results = []
        
        # store associated data for discovered hosts in array for oN, oJ, etc'
        self.hosts = []

    @property
    def ignore_http_codes(self):
        return self._ignore_http_codes

    @ignore_http_codes.setter
    def ignore_http_codes(self, codes):
        self._ignore_http_codes = [int(code) for code in codes.replace(' ', '').split(',')]


    def scan(self):
        if not self.base_host:
            self.base_host = self.target

        if not self.real_port:
            self.real_port = self.port

        for virtual_host in self.wordlist:
            hostname = virtual_host.replace('%s', self.base_host)

            if self.add_waf_bypass_headers:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                    'Host': hostname if self.real_port == 80 else '{}:{}'.format(hostname, self.real_port),
                    'Accept': '*/*',
                    'X-Originating-IP': '127.0.0.1',
                    'X-Forwarded-For': '127.0.0.1',
                    'X-Remote-IP': '127.0.0.1',
                    'X-Remote-Addr': '127.0.0.1'
                }
            else:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
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
            
        #rate limit the connection, if the int is 0 it is ignored
        time.sleep(self.rate_limit)

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
