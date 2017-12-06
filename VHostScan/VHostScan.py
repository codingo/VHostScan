#!/usr/bin/python

import sys
import dns.resolver
from argparse import ArgumentParser
from socket import gethostbyaddr
from pkg_resources import resource_filename
from .lib.core.virtual_host_scanner import *
from .lib.helpers.output_helper import *
from .lib.helpers.file_helper import load_random_user_agents
from .lib.helpers.wordlist_helper import WordList
from .lib.core.__version__ import __version__
from .lib.input import cli_argument_parser

DEFAULT_WORDLIST_FILE = resource_filename(
    'VHostScan', 'wordlists/virtual-host-scanning.txt')


def print_banner():
    print("+-+-+-+-+-+-+-+-+-+  v. %s" % __version__)
    print("|V|H|o|s|t|S|c|a|n|  Developed by @codingo_ & @__timk")
    print("+-+-+-+-+-+-+-+-+-+  https://github.com/codingo/VHostScan\n")


def main():
    print_banner()

    parser = cli_argument_parser()
    arguments = parser.parse(sys.argv[1:])

    wordlist_helper = WordList()
    wordlist, wordlist_types = wordlist_helper.get_wordlist(
        arguments.wordlists, arguments.prefix, arguments.suffix)

    if len(wordlist) == 0:
        print("[!] No words found in provided wordlists, unable to scan.")
        sys.exit(1)

    print(
        "[+] Starting virtual host scan for {host} using "
        "port {port} and {inputs}".format(
            host=arguments.target_hosts,
            port=arguments.port,
            inputs=', '.join(wordlist_types),
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
                if arguments.verbose:
                    print("[!] Discovered {host}/{ip}. Adding...".
                          format(ip=str(ip), host=host))
        except (dns.resolver.NXDOMAIN):
            print("[!] Couldn't find any records (NXDOMAIN)")
        except (dns.resolver.NoAnswer):
            print("[!] Couldn't find any records (NoAnswer)")

    if arguments.verbose:
        print("[>] Scanning with %s items in wordlist" % len(wordlist))

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
