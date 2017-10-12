#!/usr/bin/python

import os
import sys
import dns.resolver
from argparse import ArgumentParser
from socket import gethostbyaddr
from lib.core.virtual_host_scanner import *
from lib.helpers.output_helper import *
from lib.helpers.file_helper import get_combined_word_lists
from lib.helpers.file_helper import load_random_user_agents
from lib.core.__version__ import __version__
from lib.input import cli_argument_parser

DEFAULT_WORDLIST_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'wordlists',
    'virtual-host-scanning.txt'
)


def print_banner():
    print("+-+-+-+-+-+-+-+-+-+  v. %s" % __version__)
    print("|V|H|o|s|t|S|c|a|n|  Developed by @codingo_ & @__timk")
    print("+-+-+-+-+-+-+-+-+-+  https://github.com/codingo/VHostScan\n")


def main():
    print_banner()

    parser = cli_argument_parser()
    arguments = parser.parse(sys.argv[1:])

    wordlist = []
    word_list_types = []

    default_wordlist = DEFAULT_WORDLIST_FILE \
        if sys.stdin.isatty() else None

    if not sys.stdin.isatty():
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

    print(
        "[+] Starting virtual host scan for {host} using "
        "port {port} and {inputs}".format(
            host=arguments.target_hosts,
            port=arguments.port,
            inputs=', '.join(word_list_types),
        )
    )

    user_agents = []
    if arguments.user_agent:
        print('[>] User-Agent specified, using it.')
        user_agents = [arguments.user_agent]
    elif arguments.random_agent:
        print('[>] Random User-Agent flag set.')
        user_agents = load_random_user_agents()

    if(arguments.ssl):
        print("[>] SSL flag set, sending all results over HTTPS.")

    if(arguments.add_waf_bypass_headers):
        print("[>] WAF flag set, sending simple WAF bypass headers.")

    print("[>] Ignoring HTTP codes: {}".format(arguments.ignore_http_codes))

    if(arguments.ignore_content_length > 0):
        print(
            "[>] Ignoring Content length: {}".format(
                arguments.ignore_content_length
            )
        )

    if arguments.first_hit:
        print("[>] First hit is set.")

    if not arguments.no_lookup:
        try:
            print("[+] Resolving DNS for additional wordlist entries")
            for ip in dns.resolver.query(arguments.target_hosts, 'A'):
                host, aliases, ips = gethostbyaddr(str(ip))
                wordlist.append(str(ip))
                wordlist.append(host)
                wordlist.extend(aliases)
        except (dns.resolver.NXDOMAIN):
            print("[!] Couldn't find any records (NXDOMAIN)")
        except (dns.resolver.NoAnswer):
            print("[!] Couldn't find any records (NoAnswer)")

    scanner_args = vars(arguments)
    scanner_args.update({
        'target': arguments.target_hosts,
        'wordlist': wordlist,
        'user_agents': user_agents
    })

    scanner = virtual_host_scanner(**scanner_args)
    scanner.scan()
    output = output_helper(scanner, arguments)

    print(output.output_normal_likely())

    if(arguments.fuzzy_logic):
        print(output.output_fuzzy())

    if(arguments.output_normal):
        output.write_normal(arguments.output_normal)
        print("\n[+] Writing normal ouptut to %s" % arguments.output_normal)

    if(arguments.output_json):
        output.output_json(arguments.output_json)
        print("\n[+] Writing json output to %s" % arguments.output_json)

    if(arguments.output_grepable):
        output.output_grepable(arguments.output_grepable)
        print("\n[+] Writing grepable ouptut to %s" % arguments.output_json)


if __name__ == "__main__":
    main()
