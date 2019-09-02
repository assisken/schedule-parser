from dataclasses import dataclass
from typing import List, Dict


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


Week = Dict[int, List[Day]]


@dataclass
class Schedule:
    version: str
    schedule: Dict[str, Week]
