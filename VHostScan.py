#!/usr/bin/python

import os
import sys
from argparse import ArgumentParser
from dns.resolver import Resolver
from socket import gethostbyaddr
from lib.core.virtual_host_scanner import *
from lib.helpers.output_helper import *
from lib.helpers.file_helper import get_combined_word_lists, load_random_user_agents
from lib.core.__version__ import __version__


def print_banner():
    print("+-+-+-+-+-+-+-+-+-+  v. %s" % __version__)
    print("|V|H|o|s|t|S|c|a|n|  Developed by @codingo_ & @__timk")
    print("+-+-+-+-+-+-+-+-+-+  https://github.com/codingo/VHostScan\n")


def main():
    print_banner()
    parser = ArgumentParser()
    parser.add_argument("-t",   dest="target_hosts", required=True, help="Set a target range of addresses to target. Ex 10.11.1.1-255" )
    parser.add_argument("-w",   dest="wordlists", required=False, type=str, help="Set the wordlists to use (default ./wordlists/virtual-host-scanning.txt)", default=False)
    parser.add_argument("-b",   dest="base_host", required=False, help="Set host to be used during substitution in wordlist (default to TARGET).", default=False)
    parser.add_argument("-p",   dest="port", required=False, help="Set the port to use (default 80).", default=80)
    parser.add_argument("-r",   dest="real_port", required=False, help="The real port of the webserver to use in headers when not 80 (see RFC2616 14.23), useful when pivoting through ssh/nc etc (default to PORT).", default=False)

    parser.add_argument('--ignore-http-codes', dest='ignore_http_codes', type=str, help='Comma separated list of http codes to ignore with virtual host scans (default 404).', default='404')
    parser.add_argument('--ignore-content-length', dest='ignore_content_length', type=int, help='Ignore content lengths of specificed amount (default 0).', default=0)
    parser.add_argument('--unique-depth', dest='unique_depth', type=int, help='Show likely matches of page content that is found x times (default 1).', default=1)
    parser.add_argument("--ssl", dest="ssl",   action="store_true", help="If set then connections will be made over HTTPS instead of HTTP (default http).", default=False)
    parser.add_argument("--fuzzy-logic", dest="fuzzy_logic", action="store_true", help="If set then fuzzy match will be performed against unique hosts (default off).", default=False)
    parser.add_argument("--no-lookups", dest="no_lookup", action="store_true", help="Disable reverse lookups (identifies new targets and appends to wordlist, on by default).", default=False)
    parser.add_argument("--rate-limit", dest="rate_limit", type=int, help='Amount of time in seconds to delay between each scan (default 0).', default=0)
    parser.add_argument("--waf", dest="add_waf_bypass_headers",   action="store_true", help="If set then simple WAF bypass headers will be sent.", default=False)
    parser.add_argument("-oN",   dest="output_normal", help="Normal output printed to a file when the -oN option is specified with a filename argument." )
    parser.add_argument("-", dest="stdin", action="store_true", help="By passing a blank '-' you tell VHostScan to expect input from stdin (pipe).", default=False)
    parser.add_argument('--random-agent', dest='random_agent', action='store_true', help='If set, then each scan will use random user-agent from predefined list', default=False)
    parser.add_argument('--user-agent', dest='user_agent', type=str, help='User-agent for scans')

    arguments = parser.parse_args()    
    wordlist = []

    word_list_types = []

    default_wordlist = "./wordlists/virtual-host-scanning.txt" if not arguments.stdin else None

    if arguments.stdin:
        word_list_types.append('stdin')
        wordlist.extend(list(line for line in sys.stdin.read().splitlines()))

    combined = get_combined_word_lists(arguments.wordlists or default_wordlist)
    word_list_types.append('wordlists: {}'.format(
        ', '.join(combined['file_paths']),
    ))
    wordlist.extend(combined['words'])

    if len(wordlist) == 0:
        print("[!] No words found in provided wordlists, unable to scan.")
        sys.exit(1)

    print("[+] Starting virtual host scan for {host} using port {port} and {inputs}".format(
        host=arguments.target_hosts,
        port=arguments.port,
        inputs=', '.join(word_list_types),
    ))

    user_agents = []
    if arguments.user_agent:
        print('[>] User-Agent specified, using it')
        user_agents = [arguments.user_agent]
    elif arguments.random_agent:
        print('[>] Random User-Agent flag set')
        user_agents = load_random_user_agents()

    if(arguments.ssl):
        print("[>] SSL flag set, sending all results over HTTPS")

    if(arguments.add_waf_bypass_headers):
        print("[>] WAF flag set, sending simple WAF bypass headers")

    print("[>] Ignoring HTTP codes: %s" % (arguments.ignore_http_codes))
    
    if(arguments.ignore_content_length > 0):
        print("[>] Ignoring Content length: %s" % (arguments.ignore_content_length))

    if not arguments.no_lookup:
        for ip in Resolver().query(arguments.target_hosts, 'A'):
            host, aliases, ips = gethostbyaddr(str(ip))
            wordlist.append(str(ip))
            wordlist.append(host)
            wordlist.extend(aliases)

    scanner_args = vars(arguments)
    scanner_args.update({'target': arguments.target_hosts, 'wordlist': wordlist, 'user_agents': user_agents})
    scanner = virtual_host_scanner(**scanner_args)
    
    scanner.scan()
    output = output_helper(scanner, arguments)

    print(output.output_normal_likely())

    if(arguments.fuzzy_logic):
        print(output.output_fuzzy())

    if(arguments.output_normal):
        output.write_normal(arguments.output_normal)
        print("\n[+] Writing normal ouptut to %s" % arguments.output_normal)


if __name__ == "__main__":
    main()
