import json

from .net import Net

from dataclasses import dataclass
from typing import List

@dataclass
class Meal:
    ingredients: List[str]
    tags: List[str]
    source: str
    instructions: str
    measurements: List[str]

class MealInterface:
    @staticmethod
    def from_url(uri: str) -> Meal:
        data = Net.get(uri)

        dataJson = json.loads(data)