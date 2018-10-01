# VHostScan
A virtual host scanner that can be used with pivot tools, detect catch-all scenarios, aliases and dynamic default pages. First presented at SecTalks BNE in September 2017 ([slidedeck](https://docs.google.com/presentation/d/1KDY7bnCpCGabJn8UpmHGSb6z_hi_WGf3ETxzykTNjWY)).

[![Build Status](https://travis-ci.org/codingo/VHostScan.svg?branch=master)](https://travis-ci.org/codingo/VHostScan) [![Python 3.2|3.6](https://img.shields.io/badge/python-3.2|3.6-green.svg)](https://www.python.org/) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
 [![License](https://img.shields.io/badge/license-GPL3-_red.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![Twitter](https://img.shields.io/badge/twitter-@____timk-blue.svg)](https://twitter.com/__timk) [![Twitter](https://img.shields.io/badge/twitter-@codingo__-blue.svg)](https://twitter.com/codingo_)


## Key Benefits

* Quickly highlight unique content in catch-all scenarios
* Locate the outliers in catch-all scenarios where results have dynamic content on the page (such as the time)
* Identify aliases by tweaking the unique depth of matches
* Wordlist supports standard words and a variable to input a base hostname (for e.g. dev.%s from the wordlist would be run as dev.BASE_HOST)
* Works over HTTP and HTTPS
* Ability to set the real port of the webserver to use in headers when pivoting through ssh/nc
* Add simple response headers to bypass some WAF products
* Identify new targets by using reverse lookups and append to wordlist

## Product Comparisons

![VHOSTScan Feature Map](https://github.com/codingo/codingo.github.io/blob/master/assets/featureMap.PNG)

# Install Requirements

Install using:

```bash
$ python3 setup.py install
```

Dependencies will then be installed and VHostScan will be added to your path. If there is an issue regarding
running `python3 setup.py build_ext`, you will need to reinstall `numpy` using `pip uninstall numpy` and `pip install numpy==1.12.0`. This should resolve the issue as there are sometimes issues with numpy being installed through setup.py.

# Usage

| Argument        | Description |
| ------------- |:-------------|
| -h, --help | Display help message and exit |
| -t TARGET_HOSTS | Set the target host. |
| -b BASE_HOST   | Set host to be used during substitution in wordlist (default to TARGET).|
| -w WORDLISTS | Set the wordlist(s) to use. You may specify multiple wordlists in comma delimited format (e.g. -w "./wordlists/simple.txt, ./wordlists/hackthebox.txt" (default ./wordlists/virtual-host-scanning.txt). |
| -p PORT  | Set the port to use (default 80). |
| -r REAL_PORT | The real port of the webserver to use in headers when not 80 (see RFC2616 14.23), useful when pivoting through ssh/nc etc (default to PORT). |
| --ignore-http-codes IGNORE_HTTP_CODES | Comma separated list of http codes to ignore with virtual host scans (default 404). |
| --ignore-content-length IGNORE_CONTENT_LENGTH | Ignore content lengths of specificed amount. |
| --prefix PREFIX | Add a prefix to each item in the wordlist, to add dev-\<word\>, test-\<word\> etc |
| --suffix SUFFIX | Add a suffix to each item in the wordlist, to add \<word\>dev, \<word\>dev | 
| --first-hit | Return first successful result. Only use in scenarios where you are sure no catch-all is configured (such as a CTF). |
| --unique-depth UNIQUE_DEPTH | Show likely matches of page content that is found x times (default 1). |
| --ssl | If set then connections will be made over HTTPS instead of HTTP. |
| --fuzzy-logic | If set then all unique content replies are compared and a similarity ratio is given for each pair. This helps to isolate vhosts in situations where a default page isn't static (such as having the time on it). |
| --no-lookups | Disbale reverse lookups (identifies new targets and append to wordlist, on by default). | 
| --rate-limit | Amount of time in seconds to delay between each scan (default 0). |
| --random-agent | If set, each scan will use a random user-agent from a predefined list. |
| --user-agent | Specify a user agent to use for scans. |
| --waf | If set then simple WAF bypass headers will be sent. |
| -oN OUTPUT_NORMAL | Normal output printed to a file when the -oN option is specified with a filename argument. |
| -oG OUTPUT_GREPABLE | Grepable output printed to a file when the -oG is specified with a filename argument. |
| -oJ OUTPUT_JSON | JSON output printed to a file when the -oJ option is specified with a filename argument. |
| -v VERBOSE | Increase the output of the tool to show progress |


## Usage Examples

_Note that a number of these examples reference 10.10.10.29. This IP refers to BANK.HTB, a retired target machine from HackTheBox (https://www.hackthebox.eu/)._

### Quick Example
The most straightforward example runs the default wordlist against example.com using the default of port 80:

```bash
$ VHostScan -t example.com
```

### Quick Example with SSL
If your connection requires SSL, you can use:

```bash
$ VHostScan -t example.com --ssl
```

![VHOSTScan Wordlist example](https://github.com/codingo/codingo.github.io/blob/master/assets/Bank%20VHOST%20Example.png)

### Port forwarding
Say you have an SSH port forward listening on port 4444 fowarding traffic to port 80 on example.com's development machine. You could use the following to make VHostScan connect through your SSH tunnel via localhost:4444 but format the header requests to suit connecting straight to port 80:

```bash
$ VHostScan -t localhost -b example.com -p 4444 -r 80
```

### STDIN
VHostScan Supports piping from other applications and will treat information passed to VHostScan as wordlist data, for example:
```bash
$ cat bank.htb | VHostScan -t 10.10.10.29
```

![VHOSTScan STDIN Example](https://github.com/codingo/codingo.github.io/blob/master/assets/Bank%20VHOST%20Pipe%20Example.png)

### STDIN and WordList
You can still specify a wordlist to use along with stdin. In these cases wordlist information will be appended to stdin. For example:
```bash
$ echo -e 'a.example.com\b.example.com' | VHostScan -t localhost -w ./wordlists/wordlist.txt
```
### Fuzzy Logic
Here is an example with fuzzy logic enabled. You can see the last comparison is much more similar than the first two (it is comparing the content not the actual hashes):

![VHOSTScan Fuzzy Logic Example](https://github.com/codingo/codingo.github.io/blob/master/assets/VHostScan-Fuzzy-Wuzzy.PNG)

## Running the tests

This project includes a small battery of tests. It's really simple to run the tests:

```bash
pip install -r test-requirements.txt
pytest
```

Or you can optionally run:

```bash
pip install -r test-requirements.txt
python3 setup.py test
```

If you're thinking of adding a new feature to the project, consider also contributing with a couple of tests. A well-tested codebase is a sane codebase. :)
