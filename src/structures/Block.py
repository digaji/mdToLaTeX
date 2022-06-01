from typing import Optional
from typing_extensions import Self

class Block:

    def __init__(self, content: str, subs = None):
        self.content = content
        self.subs = subs
        pass
