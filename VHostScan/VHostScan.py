#!/usr/bin/python

import os
import sys
from argparse import ArgumentParser

try:
    from lib.core.virtual_host_scanner import *

except KeyboardInterrupt:
    print("user aborted")
    raise SystemExit

except ModuleNotFoundError:
    print("Not all modules could be loaded. Please reclone from the master branch on https://github.com/codingo/VHostScan or use a tagged release.")
    raise SystemExit

def print_banner():
    print("+-+-+-+-+-+-+-+-+-+  v. 0.1")
    print("|V|H|o|s|t|S|c|a|n|  Developed by @codingo_ & @__timk")
    print("+-+-+-+-+-+-+-+-+-+  https://github.com/codingo/VHostScan")


def main():
    parser = ArgumentParser()
    parser.add_argument("-t",   dest="target_hosts", required=True, help="Set a target range of addresses to target. Ex 10.11.1.1-255" )
    parser.add_argument("-o",   dest="output_directory", required=True, help="Set the output directory. Ex /root/Documents/labs/")
    parser.add_argument("-w",   dest="wordlist", required=False, help="Set the wordlist to use for generated commands. Ex /usr/share/wordlist.txt", default="./wordlists/virtual-host-scanning.txt")
    parser.add_argument("-p",   dest="port", required=False, help="Set the port to use. Leave blank to use discovered ports. Useful to force virtual host scanning on non-standard webserver ports (default 80).", default=80)

    parser.add_argument('--ignore-http-codes', dest='ignore_http_codes', type=str, help='Comma separated list of http codes to ignore with virtual host scans (default 404).', default='404')
    parser.add_argument('--ignore-content-length', dest='ignore_content_length', type=int, help='Ignore content lengths of specificed amount. This may become useful when a server returns a static page on every virtual host guess.', default=0)
    parser.add_argument('--unique-depth', dest='unique_depth', type=int, help='Show likely matches of page content that is found x times (default 1).', default=1)
    arguments = parser.parse_args()

    if len(sys.argv) == 1:
        print_banner()
        parser.error("No arguments given.")
        parser.print_usage
        sys.exit()

    if arguments.output_directory.endswith('/' or '\\'):
        arguments.output_directory = arguments.output_directory[:-1]
    if arguments.target_hosts.endswith('/' or '\\'):
        arguments.target_hosts = arguments.target_hosts[:-1]

    print_banner()

    scanner = virtual_host_scanner(arguments.target_hosts, arguments.output_directory, arguments.port, arguments.unique_depth, arguments.ignore_http_codes, arguments.ignore_content_length, arguments.wordlist)
    scanner.scan()
    scanner.show_likely_matches()

if __name__ == "__main__":
    main()