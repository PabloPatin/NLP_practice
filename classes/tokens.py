from dataclasses import dataclass
from functools import total_ordering
from typing import TypeAlias

Tid: TypeAlias = int


@total_ordering
@dataclass
class Token:
    """Class token join token_id (Tid) and unique word in corpus text.
    It also contains the number of times it occurs in the text and may be compared by it value"""
    tid: Tid
    quantity: int
    value: str

    def __eq__(self, other):
        return self.quantity == other.quantity

    def __lt__(self, other):
        return self.quantity < other.quantity

    def __add__(self, other: int):
        self.quantity += 1
        return self


@dataclass
class Bigram(Token):
    """A token that contains a dictionary of Tid tokens that can go after it"""
    tail: dict[Tid:int]


@dataclass
class Trigram(Bigram):
    """A couple of tokens that contains a dict of Tid tokens that can go after it"""
    tid: tuple[Tid, Tid]
