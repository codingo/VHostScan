import os
import requests
import hashlib
from math import floor
import time
import threading
import pandas as pd
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
     
    def __init__(self, target, base_host, wordlist,ratelimit, port=80, real_port=80, ssl=False, unique_depth=1, ignore_http_codes='404', ignore_content_length=0, fuzzy_logic=False, add_waf_bypass_headers=False):
        self.target = target
        self.base_host = base_host
        self.port = int(port)
        self.real_port = int(real_port)
        self.ignore_http_codes = list(map(int, ignore_http_codes.replace(' ', '').split(',')))
        self.ignore_content_length = ignore_content_length
        self.wordlist = wordlist
        self.ratelimit = ratelimit
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

    def rate_limited(period=1, every=1.0):
        '''
        Prevent a method from being called
        if it was previously called before
        a time widows has elapsed.
        :param int period: Maximum method invocations within a period. Must be greater than 0.
        :param float every: A dampening factor (in seconds). Can be any number greater than 0.
        :return: Decorated function that will forward method invocations if the time window has elapsed.
        :rtype: function
        '''
        frequency = abs(every) / float(clamp(period))

        def decorator(func):
            '''
            Extend the behaviour of the following
            function, forwarding method invocations
            if the time window hes elapsed.
            :param function func: The function to decorate.
            :return: Decorated function.
            :rtype: function
            '''

            # To get around issues with function local scope
            # and reassigning variables, we wrap the time
            # within a list. When updating the value we're
            # not reassigning `last_called`, which would not
            # work, but instead reassigning the value at a
            # particular index.
            last_called = [0.0]

            # Add thread safety
            lock = threading.RLock()

            def wrapper(*args, **kargs):
                '''Decorator wrapper function'''
                with lock:
                    elapsed = time.time() - last_called[0]
                    left_to_wait = frequency - elapsed
                    if left_to_wait > 0:
                        time.sleep(left_to_wait)
                    last_called[0] = time.time()
                return func(*args, **kargs)

            return wrapper

        return decorator

    def clamp(value):
        '''
        Clamp integer between 1 and max
        There must be at least 1 method invocation
        made over the time period. Make sure the
        value passed is at least 1 and is not a
        fraction of an invocation.
        :param float value: The number of method invocations.
        :return: Clamped number of invocations.
        :rtype: int
        '''
        return max(1, min(sys.maxsize, floor(value)))

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

            rate_limited(self.ratelimit)
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
