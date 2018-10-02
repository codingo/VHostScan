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
from .lib.helpers.color_helper import *

DEFAULT_WORDLIST_FILE = resource_filename(
    'VHostScan', 'wordlists/virtual-host-scanning.txt')


def print_banner():
    board_edge = t_white("+-+-+-+-+-+-+-+-+-+")
    board_text = ''
    for i, c in enumerate("|V|H|o|s|t|S|c|a|n|"):
        if i % 2 == 0:
            board_text += t_white(c)
        else:
            board_text += t_yellow(c)

    version = t_green("  v. %s" % __version__)
    developer = t_green("  Developed by @codingo_ & @__timk")
    repo = t_green("  https://github.com/codingo/VHostScan")

    print(board_edge, version)
    print(board_text, developer)
    print(board_edge, repo)
    print()


def extract_arguments():
    parser = cli_argument_parser()
    return parser.parse(sys.argv[1:])


def main():
    arguments = extract_arguments()

    config_colorization(arguments.use_color)

    print_banner()

    wordlist_helper = WordList()
    wordlist, wordlist_types = wordlist_helper.get_wordlist(
        arguments.wordlists, arguments.prefix, arguments.suffix)

    if len(wordlist) == 0:
        print(t_error(
            "[!] No words found in provided wordlists, unable to scan."
        ), end='')
        sys.exit(1)

    print(t_process(
        "[+] Starting virtual host scan for {host} using "
        "port {port} and {inputs}".format(
            host=arguments.target_hosts,
            port=arguments.port,
            inputs=', '.join(wordlist_types),
        )
    ))

    user_agents = []
    if arguments.user_agent:
        print(t_process('[>] User-Agent specified, using it.'))
        user_agents = [arguments.user_agent]
    elif arguments.random_agent:
        print(t_process('[>] Random User-Agent flag set.'))
        user_agents = load_random_user_agents()

    if(arguments.ssl):
        print(t_process("[>] SSL flag set, sending all results over HTTPS."))

    if(arguments.add_waf_bypass_headers):
        print(t_process(
            "[>] WAF flag set, sending simple WAF bypass headers."
        ))

    print(t_process(
        "[>] Ignoring HTTP codes: {}".format(arguments.ignore_http_codes)
    ))

    if(arguments.ignore_content_length > 0):
        print(t_process(
            "[>] Ignoring Content length: {}".format(
                arguments.ignore_content_length
            )
        ))

    if arguments.first_hit:
        print(t_process("[>] First hit is set."))

    if not arguments.no_lookup:
        try:
            print(t_process(
                "[+] Resolving DNS for additional wordlist entries"
            ))
            for ip in dns.resolver.query(arguments.target_hosts, 'A'):
                host, aliases, ips = gethostbyaddr(str(ip))
                wordlist.append(str(ip))
                wordlist.append(host)
                wordlist.extend(aliases)
                if arguments.verbose:
                    print(t_error("[!] Discovered {host}/{ip}. Adding...".
                          format(ip=str(ip), host=host)))
        except (dns.resolver.NXDOMAIN):
            print(t_error("[!] Couldn't find any records (NXDOMAIN)"))
        except (dns.resolver.NoAnswer):
            print(t_error("[!] Couldn't find any records (NoAnswer)"))

    if arguments.verbose:
        print(t_process(
            "[>] Scanning with %s items in wordlist" % len(wordlist)
        ))

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
        print(t_process(output.output_fuzzy()))

    if(arguments.output_normal):
        output.write_normal(arguments.output_normal)
        print(t_process(
            "\n[+] Writing normal ouptut to %s" % arguments.output_normal
        ))

    if(arguments.output_json):
        output.output_json(arguments.output_json)
        print(t_process(
            "\n[+] Writing json output to %s" % arguments.output_json
        ))

    if(arguments.output_grepable):
        output.output_grepable(arguments.output_grepable)
        print(t_process(
            "\n[+] Writing grepable ouptut to %s" % arguments.output_json
        ))


if __name__ == "__main__":
    main()
