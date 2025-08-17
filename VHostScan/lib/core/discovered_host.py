from typing import List


class discovered_host(object):
    """
    Auxiliary class used for storing discovered hosts
    """

    def __init__(self):
        self.hostname: str = ''
        self.response_code: int = 0
        self.hash: str = ''
        self.keys: List[str] = []
        self.content: bytes = b''
