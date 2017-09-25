#!/usr/bin/python

import os
import sys
from argparse import ArgumentParser
from lib.core.virtual_host_scanner import *
from lib.helpers.output_helper import *


def print_banner():
    print("+-+-+-+-+-+-+-+-+-+  v. 0.4")
    print("|V|H|o|s|t|S|c|a|n|  Developed by @codingo_ & @__timk")
    print("+-+-+-+-+-+-+-+-+-+  https://github.com/codingo/VHostScan\n")


def main():
    print_banner()
    parser = ArgumentParser()
    parser.add_argument("-t",   dest="target_hosts", required=True, help="Set a target range of addresses to target. Ex 10.11.1.1-255" )
    parser.add_argument("-w",   dest="wordlist", required=False, type=str, help="Set the wordlist to use (default ./wordlists/virtual-host-scanning.txt)")
    parser.add_argument("-b",   dest="base_host", required=False, help="Set host to be used during substitution in wordlist (default to TARGET).", default=False)
    parser.add_argument("-p",   dest="port", required=False, help="Set the port to use (default 80).", default=80)
    parser.add_argument("-r",   dest="real_port", required=False, help="The real port of the webserver to use in headers when not 80 (see RFC2616 14.23), useful when pivoting through ssh/nc etc (default to PORT).", default=False)

    parser.add_argument('--ignore-http-codes', dest='ignore_http_codes', type=str, help='Comma separated list of http codes to ignore with virtual host scans (default 404).', default='404')
    parser.add_argument('--ignore-content-length', dest='ignore_content_length', type=int, help='Ignore content lengths of specificed amount (default 0).', default=0)
    parser.add_argument('--unique-depth', dest='unique_depth', type=int, help='Show likely matches of page content that is found x times (default 1).', default=1)
    parser.add_argument("--ssl", dest="ssl",   action="store_true", help="If set then connections will be made over HTTPS instead of HTTP (default http).", default=False)
    parser.add_argument("-oN",   dest="output_normal", help="Normal output printed to a file when the -oN option is specified with a filename argument." )
    parser.add_argument("-", dest="stdin", action="store_true", help="By passing a blank '-' you tell VHostScan to expect input from stdin (pipe).", default=False)
    
    arguments = parser.parse_args()    
    wordlist = ""
    
    if(arguments.stdin):
        for line in sys.stdin:
            wordlist += line
    elif(arguments.stdin and arguments.wordlist):
        if not os.path.exists(arguments.wordlist):
            print("[!] Wordlist %s doesn't exist and can't be appended  to stdin." % arguments.wordlistt)
        else:
            wordlist += open(arguments.wordlist).read().splitlines()    
    else:
        wordlist = open("./wordlists/virtual-host-scanning.txt").read().splitlines()   

    print("[+] Starting virtual host scan for %s using port %s and wordlist %s" % (arguments.target_hosts, 
                                                                                   str(arguments.port), 
                                                                                   "placeholder"))
    
    if(arguments.ssl):
        print("[>] SSL flag set, sending all results over HTTPS")

    print("[>] Ignoring HTTP codes: %s" % (arguments.ignore_http_codes))
    
    if(arguments.ignore_content_length > 0):
        print("[>] Ignoring Content length: %s" % (arguments.ignore_content_length))

    scanner = virtual_host_scanner( arguments.target_hosts, arguments.base_host, wordlist, arguments.port, arguments.real_port, arguments.ssl, 
                                    arguments.unique_depth, arguments.ignore_http_codes, arguments.ignore_content_length)
    
    scanner.scan()
    output = output_helper(scanner)

    print(output.output_normal_likely())

    if(arguments.output_normal):
        output.write_normal(arguments.output_normal)
        print("\n[+] Writing normal ouptut to %s" % arguments.output_normal)


if __name__ == "__main__":
    main()
