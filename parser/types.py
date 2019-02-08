from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    time: str
    item_type: str
    name: str
    place: str
    teachers: List[str]


@dataclass
class Day:
    day: str
    date: str
    items: List[Item]


@dataclass
class Week:
    week: int
    days: List[Day]
