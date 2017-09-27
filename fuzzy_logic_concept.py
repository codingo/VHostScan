#!/usr/bin/env python3

import requests
import hashlib
import itertools
from fuzzywuzzy import fuzz

headers = ('lol', 'intranet.example.com', 'dev.example.com')

request_data = {}

for host in headers:
    headers = { 'Host': host }
    req = requests.get('http://home.kent.id.au', headers=headers, verify=False)
    hash = hashlib.sha256(req.text.encode('utf-8')).hexdigest()
    request_data[hash] = req.content

for a, b in itertools.combinations(request_data.keys(), 2):
    print('%s is %s percent similar to %s' % (a, fuzz.ratio(request_data[a], request_data[b]), b))
