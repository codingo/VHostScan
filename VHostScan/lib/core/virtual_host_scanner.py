import hashlib
import os
import random
import time

import requests
import urllib3

import pandas as pd

from .discovered_host import discovered_host

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '\
                     'AppleWebKit/537.36 (KHTML, like Gecko) '\
                     'Chrome/61.0.3163.100 Safari/537.36'

try:
    assert requests.__version__ != "2.18.0"
    import requests.packages.urllib3.util.ssl_ as ssl_
    import requests.packages.urllib3.connection as connection
except (ImportError, AssertionError, AttributeError):
    import urllib3.util.ssl_ as ssl_
    import urllib3.connection as connection

# print("Using requests " + requests.__version__)

_target_host = None


def _ssl_wrap_socket(sock, keyfile=None, certfile=None, cert_reqs=None,
                     ca_certs=None, server_hostname=None,
                     ssl_version=None, ciphers=None, ssl_context=None,
                     ca_cert_dir=None):
    return ssl_.ssl_wrap_socket(sock, keyfile=keyfile, certfile=certfile,
                                cert_reqs=cert_reqs, ca_certs=ca_certs,
                                server_hostname=_target_host,
                                ssl_version=ssl_version, ciphers=ciphers,
                                ssl_context=ssl_context,
                                ca_cert_dir=ca_cert_dir)

connection.ssl_wrap_socket = _ssl_wrap_socket


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
        self.user_agents = list(kwargs.get('user_agents')) \
            or [DEFAULT_USER_AGENT]

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

        for virtual_host in self.wordlist:
            hostname = virtual_host.replace('%s', self.base_host)

            if self.verbose:
                print("[*] Scanning {hostname}".format(hostname=hostname))

            if self.real_port == 80:
                host_header = hostname
            else:
                host_header = '{}:{}'.format(hostname, self.real_port)

            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Host': host_header,
                'Accept': '*/*'
            }

            if self.add_waf_bypass_headers:
                headers.update({
                    'X-Originating-IP': '127.0.0.1',
                    'X-Forwarded-For': '127.0.0.1',
                    'X-Remote-IP': '127.0.0.1',
                    'X-Remote-Addr': '127.0.0.1'
                })

            dest_url = '{}://{}:{}/'.format(
                'https' if self.ssl else 'http',
                self.target,
                self.port
            )

            _target_host = hostname

            try:
                res = requests.get(dest_url, headers=headers, verify=False)
            except requests.exceptions.RequestException:
                continue

            if res.status_code in self.ignore_http_codes:
                continue

            response_length = int(res.headers.get('content-length', 0))
            if self.ignore_content_length and \
               self.ignore_content_length == response_length:
                continue

            # hash the page results to aid in identifing unique content
            page_hash = hashlib.sha256(res.text.encode('utf-8')).hexdigest()

            self.hosts.append(self.create_host(res, hostname, page_hash))

            # add url and hash into array for likely matches
            self.results.append(hostname + ',' + page_hash)

            if len(self.hosts) >= 1 and self.first_hit:
                break

            # rate limit the connection, if the int is 0 it is ignored
            time.sleep(self.rate_limit)

        self.completed_scan = True

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
        host.contnet = response.content

        for key, val in response.headers.items():
            output += '  {}: {}\n'.format(key, val)
            host.keys.append('{}: {}'.format(key, val))

        print(output)

        return host
