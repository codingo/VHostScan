import hashlib
import os
import random
import time
import warnings
from typing import List, Optional, Dict, Any

import requests
import urllib3

import pandas as pd

from .discovered_host import discovered_host

# Disable urllib3 warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
                     'AppleWebKit/537.36 (KHTML, like Gecko) '\
                     'Chrome/120.0.0.0 Safari/537.36'


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
        self.ssl = kwargs.get('ssl', False)
        self.fuzzy_logic = kwargs.get('fuzzy_logic', False)
        self.unique_depth = int(kwargs.get('unique_depth', 1))
        self.ignore_http_codes = kwargs.get('ignore_http_codes', '404')
        self.first_hit = kwargs.get('first_hit')
        self.verbose = kwargs.get('verbose')

        self.ignore_content_length = int(
            kwargs.get('ignore_content_length', 0)
        )

        self.add_waf_bypass_headers = kwargs.get(
            'add_waf_bypass_headers',
            False
        )

        # this can be made redundant in future with better exceptions
        self.completed_scan = False

        # this is maintained until likely-matches is refactored to use
        # new class
        self.results = []

        # store associated data for discovered hosts
        # in array for oN, oJ, etc'
        self.hosts = []

        # available user-agents
        user_agents_arg = kwargs.get('user_agents')
        if user_agents_arg:
            self.user_agents = list(user_agents_arg)
        else:
            self.user_agents = [DEFAULT_USER_AGENT]

    @property
    def ignore_http_codes(self):
        return self._ignore_http_codes

    @ignore_http_codes.setter
    def ignore_http_codes(self, codes):
        self._ignore_http_codes = [
            int(code) for code in codes.replace(' ', '').split(',')
        ]

    def scan(self):
        if not self.base_host:
            self.base_host = self.target

        if not self.real_port:
            self.real_port = self.port

        total_hosts = len(self.wordlist)
        scanned_count = 0

        for virtual_host in self.wordlist:
            scanned_count += 1
            hostname = virtual_host.replace('%s', self.base_host)

            if self.verbose:
                progress = f"[{scanned_count}/{total_hosts}]"
                print(f"[*] {progress} Scanning {hostname}")

            if self.real_port == 80 and not self.ssl:
                host_header = hostname
            elif self.real_port == 443 and self.ssl:
                host_header = hostname
            else:
                host_header = f'{hostname}:{self.real_port}'

            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Host': host_header,
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }

            if self.add_waf_bypass_headers:
                headers.update({
                    'X-Originating-IP': '127.0.0.1',
                    'X-Forwarded-For': '127.0.0.1',
                    'X-Remote-IP': '127.0.0.1',
                    'X-Remote-Addr': '127.0.0.1',
                    'X-Forwarded-Host': hostname,
                    'X-Forwarded-Proto': 'https' if self.ssl else 'http'
                })

            dest_url = f"{'https' if self.ssl else 'http'}://{self.target}:{self.port}/"

            try:
                # Set timeout and improved error handling
                res = requests.get(
                    dest_url, 
                    headers=headers, 
                    verify=False, 
                    timeout=10,
                    allow_redirects=True,
                    stream=False
                )
            except requests.exceptions.Timeout:
                if self.verbose:
                    print(f"[!] Timeout for {hostname}")
                continue
            except requests.exceptions.ConnectionError:
                if self.verbose:
                    print(f"[!] Connection error for {hostname}")
                continue
            except requests.exceptions.RequestException as e:
                if self.verbose:
                    print(f"[!] Request error for {hostname}: {e}")
                continue

            if res.status_code in self.ignore_http_codes:
                continue

            # Better content length handling
            response_length = len(res.content) if res.content else 0
            content_length_header = res.headers.get('content-length')
            if content_length_header:
                try:
                    response_length = int(content_length_header)
                except ValueError:
                    pass

            if self.ignore_content_length and \
               self.ignore_content_length == response_length:
                continue

            # Hash the page results to aid in identifying unique content
            try:
                page_content = res.text if res.text else ''
                page_hash = hashlib.sha256(page_content.encode('utf-8')).hexdigest()
            except UnicodeDecodeError:
                # Fallback for binary content
                page_hash = hashlib.sha256(res.content).hexdigest()

            self.hosts.append(self.create_host(res, hostname, page_hash))

            # Add url and hash into array for likely matches
            self.results.append(f"{hostname},{page_hash}")

            if len(self.hosts) >= 1 and self.first_hit:
                break

            # Rate limit the connection, if the int is 0 it is ignored
            if self.rate_limit > 0:
                time.sleep(self.rate_limit)

        self.completed_scan = True
        
        if self.verbose:
            print(f"\n[+] Scan completed. Found {len(self.hosts)} unique hosts.")

    def likely_matches(self):
        if self.completed_scan is False:
            print("[!] Likely matches cannot be printed "
                  "as a scan has not yet been run.")
            return

        # segment results from previous scan into usable results
        segmented_data = {}
        for item in self.results:
            result = item.split(",")
            segmented_data[result[0]] = result[1]

        dataframe = pd.DataFrame([
            [key, value] for key, value in segmented_data.items()],
            columns=["key_col", "val_col"]
        )

        segmented_data = dataframe.groupby("val_col").filter(
            lambda x: len(x) <= self.unique_depth
        )

        return segmented_data["key_col"].values.tolist()

    def create_host(self, response, hostname, page_hash):
        """
        Creates a host using the responce and the hash.
        Prints current result in real time.
        """
        output = '[#] Found: {} (code: {}, length: {}, hash: {})\n'.format(
            hostname,
            response.status_code,
            response.headers.get('content-length'),
            page_hash
        )

        host = discovered_host()
        host.hostname = hostname
        host.response_code = response.status_code
        host.hash = page_hash
        host.content = response.content

        for key, val in response.headers.items():
            output += '  {}: {}\n'.format(key, val)
            host.keys.append('{}: {}'.format(key, val))

        print(output)

        return host
