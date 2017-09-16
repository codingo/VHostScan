from lib.core.discovered_host import *

class output_normal(object):
    def __init__(self):
        self.hosts = []

    def print_current(self):
        for p in self.hosts: print ("[!!!!] %s (%s) hash: %s" % (p.hostname, p.response_code, p.hash))
