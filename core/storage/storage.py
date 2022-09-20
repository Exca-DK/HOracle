

from collections import deque
from typing import Dict


class Storage:

    def __init__(self) -> None:
        self.Storage: Dict[deque] = {}