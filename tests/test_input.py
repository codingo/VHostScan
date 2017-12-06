import argparse
import pytest

from VHostScan.lib.input import cli_argument_parser

def test_parse_arguments_default_value(tmpdir):
    words = ['word1', 'word2', 'word3']
    wordlist = tmpdir.mkdir('test_command').join('default')
    wordlist.write('\n'.join(words))

    argv = ['-t', 'myhost']
    
    arguments = cli_argument_parser().parse(argv)

    expected_arguments = {
        'target_hosts': 'myhost',
        'wordlists': None,
        'base_host': False,
        'port': 80,
        'real_port': False,
        'ignore_http_codes': '404',
        'ignore_content_length': 0,
        'first_hit': False,
        'unique_depth': 1,
        'fuzzy_logic': False,
        'no_lookup': False,
        'rate_limit': 0,
        'random_agent': False,
        'user_agent': None,
        'add_waf_bypass_headers': False,
        'output_normal': None,
        'output_json': None,
        'output_grepable' : None,
        'ssl': False,
        'prefix': False,
        'suffix': False,
        'verbose': False
    }
    
    assert vars(arguments) == expected_arguments


def test_parse_arguments_custom_arguments(tmpdir):
    words = ['some', 'other', 'words']
    wordlist = tmpdir.mkdir('test_command').join('other_words')
    wordlist.write('\n'.join(words))

    argv = [
        '-t', '10.11.1.1',
        '-w', str(wordlist),
        '-b', 'myhost',
        '-p', '8000',
        '-r', '8001',
        '--ignore-http-codes', '400,500,302',
        '--ignore-content-length', '100',
        '--unique-depth', '5',
        '--first-hit',
        '--ssl',
        '--fuzzy-logic',
        '--no-lookups',
        '--rate-limit', '10',
        '--user-agent', 'some-user-agent',
        '--waf',
        '-oN', '/tmp/on',
        '--prefix','dev-',
        '--suffix','test',
        '-v'
    ]

    arguments = cli_argument_parser().parse(argv)

    expected_arguments = {
        'target_hosts': '10.11.1.1',
        'wordlists': str(wordlist),
        'base_host': 'myhost',
        'port': 8000,
        'real_port': 8001,
        'ignore_http_codes': '400,500,302',
        'ignore_content_length': 100,
        'first_hit': True,
        'unique_depth': 5,
        'ssl': True,
        'fuzzy_logic': True,
        'no_lookup': True,
        'rate_limit': 10,
        'user_agent': 'some-user-agent',
        'random_agent': False,
        'add_waf_bypass_headers': True,
        'output_normal': '/tmp/on',
        'output_json': None,
        'output_grepable' : None,
        'prefix': 'dev-',
        'suffix': 'test',
        'verbose': True
    }

    assert vars(arguments) == expected_arguments

def test_parse_arguments_mutually_exclusive_user_agent():
    argv = [
        '-t', '10.11.1.1',
        '--user-agent', 'my-user-agent',
        '--random-agent',
    ]

    with pytest.raises(SystemExit):
        cli_argument_parser().parse(argv)

def test_parse_arguments_mutually_exclusive_output():
    argv = [
        '-t', '10.11.1.1',
        '-oJ',
        '-oN',
    ]

    with pytest.raises(SystemExit):
        cli_argument_parser().parse(argv)

def test_parse_arguments_unknown_argument():
    argv = [
        '-t', '10.11.1.1',
        '-i-do-not-exist',
    ]

    with pytest.raises(SystemExit):
        cli_argument_parser().parse(argv)
