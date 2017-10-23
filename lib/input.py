from argparse import ArgumentParser


class cli_argument_parser(object):
    def __init__(self):
        self._parser = self.setup_parser()

    def parse(self, argv):
        return self._parser.parse_args(argv)

    @staticmethod
    def setup_parser():
        parser = ArgumentParser()

        parser.add_argument(
            '-t', dest='target_hosts', required=True,
            help='Set a target range of addresses to target. Ex 10.11.1.1-255'
        ),

        parser.add_argument(
            '-w', dest='wordlists',
            help='Set the wordlists to use (default '
                 './wordlists/virtual-host-scanning.txt)'
        )

        parser.add_argument(
            '-b', dest='base_host', default=False,
            help='Set host to be used during substitution in '
                 'wordlist (default to TARGET).'
        )

        parser.add_argument(
            '-p', dest='port', default=80, type=int,
            help='Set the port to use (default 80).'
        )

        parser.add_argument(
            '--prefix', dest='prefix', default=False,
            help='Add a prefix to each item in the word list (dev, test etc)'
        )

        parser.add_argument(
            '--suffix', dest='suffix', default=False,
            help='Add a suffix to each item in the word list'
        )

        parser.add_argument(
            '-r', dest='real_port', type=int, default=False,
            help='The real port of the webserver to use in headers when '
                 'not 80 (see RFC2616 14.23), useful when pivoting through '
                 'ssh/nc etc (default to PORT).'
        )

        parser.add_argument(
            '--ignore-http-codes', dest='ignore_http_codes', default='404',
            help='Comma separated list of http codes to ignore with virtual '
                 'host scans (default 404).'
        )

        parser.add_argument(
            '--ignore-content-length', dest='ignore_content_length', type=int,
            default=0, help='Ignore content lengths of specificed amount '
                            '(default 0).'
        )

        parser.add_argument(
            '--first-hit', dest='first_hit', action='store_true',
            default=False,
            help='Return first successful result. Only use in scenarios where '
                 'you are sure no catch-all is configured (such as a CTF).'
        )

        parser.add_argument(
            '--unique-depth', dest='unique_depth', type=int, default=1,
            help='Show likely matches of page content that is found x times '
                 '(default 1).'
        )

        parser.add_argument(
            '--ssl', dest='ssl', action='store_true', default=False,
            help='If set then connections will be made over HTTPS instead of '
                 'HTTP (default http).'
        )

        parser.add_argument(
            '--fuzzy-logic', dest='fuzzy_logic', action='store_true',
            default=False,
            help='If set then fuzzy match will be performed against unique '
                 'hosts (default off).'
        )

        parser.add_argument(
            '--no-lookups', dest='no_lookup', action='store_true',
            default=False,
            help='Disable reverse lookups (identifies new targets and appends '
                 'to wordlist, on by default).'
        )

        parser.add_argument(
            '--rate-limit', dest='rate_limit', type=int, default=0,
            help='Amount of time in seconds to delay between each scan '
                 '(default 0).'
        )

        parser.add_argument(
            '--waf', dest='add_waf_bypass_headers', action='store_true',
            default=False,
            help='If set then simple WAF bypass headers will be sent.'
        )

        parser.add_argument(
            '-v', dest='verbose', action='store_true', default=False,
            help='Print verbose output'
        )

        output = parser.add_mutually_exclusive_group()
        output.add_argument(
            '-oN', dest='output_normal',
            help='Normal output printed to a file when the -oN option is '
                 'specified with a filename argument.'
        )

        output.add_argument(
            '-oJ', dest='output_json',
            help='JSON output printed to a file when the -oJ option is '
                 'specified with a filename argument.'
        )

        output.add_argument(
            '-oG', dest='output_grepable',
            help='Grepable output printed to a file when the -oG option is '
                 'specified with a filename argument.'
        )

        user_agent = parser.add_mutually_exclusive_group()
        user_agent.add_argument(
            '--random-agent', dest='random_agent', action='store_true',
            default=False, help='If set, then each scan will use random '
                                'user-agent from predefined list.'
        )

        user_agent.add_argument(
            '--user-agent', dest='user_agent',
            help='Specify a user-agent to use for scans'
        )

        return parser
