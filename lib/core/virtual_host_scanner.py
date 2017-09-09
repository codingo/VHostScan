import os
import requests
import hashlib
import pandas as pd

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
     
    def __init__(self, target, port=80, unique_depth=1, ignore_http_codes='404', ignore_content_length=0, 
                 wordlist="./wordlists/virtual-host-scanning.txt"):
        self.target = target
        self.port = port
        self.ignore_http_codes = list(map(int, ignore_http_codes.replace(' ', '').split(',')))
        self.ignore_content_length = ignore_content_length
        self.wordlist = wordlist
        self.unique_depth = unique_depth
        
        self.completed_scan=False
        self.results = []

    def scan(self):
        print("[+] Starting virtual host scan for %s using port %s and wordlist %s" % (self.target, str(self.port), self.wordlist))
        print("[>] Ignoring HTTP codes: %s" % (self.ignore_http_codes))
        if(self.ignore_content_length > 0):
            print("[>] Ignoring Content length: %s" % (self.ignore_content_length))

        if not os.path.exists(self.wordlist):
            print("[!] Wordlist %s doesn't exist, ending scan." % self.wordlist)
            return
        
        virtual_host_list = open(self.wordlist).read().splitlines()

        for virtual_host in virtual_host_list:
            hostname = virtual_host.replace('%s', self.target)

            headers = {
                'Host': hostname if self.port == 80 else '{}:{}'.format(hostname, self.port),
                'Accept': '*/*'
            }
            
            # todo: to be made redundant/replaced with a --ssl flag? Current implementation limits ssl severely
            dest_url = '{}://{}:{}/'.format('https' if int(self.port) == 443 else 'http', self.target, self.port)

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
            output = '[#] Found: {} (code: {}, length: {}, hash: {})'.format(hostname, res.status_code, 
                                                                             res.headers.get('content-length'), page_hash)

            # print current results
            print(output)
            for key, val in res.headers.items():
                output = '  {}: {}'.format(key, val)
                print(output)
            
            # add url and hash into array for likely matches
            self.results.append(hostname + ',' + page_hash)

        self.completed_scan=True


    def likely_matches(self):
        if self.completed_scan is False:
            print("Likely matches cannot be printed as a scan has not yet been run.")
            return      

        print("\n[#] Most likely matches with a unique count of %s or less:" % self.unique_depth)

        d={}

        for item in self.results:
            r=item.split(",")
            d[r[0]]=r[1]

        df= pd.DataFrame([[key, value] for key, value in d.items()], columns=["key_col", "val_col"])
        d=df.groupby("val_col").filter(lambda x: len(x) <= self.unique_depth)
        matches=((d["key_col"].values).tolist())

        return matches