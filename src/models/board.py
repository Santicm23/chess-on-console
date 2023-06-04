
from dataclasses import dataclass, field
from typing import List, Iterable


@dataclass(slots=True)
class Board:
    matrix: List[List] = field(default_factory = lambda: [[None for _ in range(8)] for _ in range(8)])

    def __str__(self) -> str:...

    def __repr__(self) -> str:...

    def __getitem__(self, pos: Iterable[int]):...

    def __setitem__(self, pos: Iterable[int], piece):...

    def __delitem__(self, pos: Iterable[int]):...

    def __iter__(self):...