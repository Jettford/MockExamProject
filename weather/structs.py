from dataclasses import dataclass

from typing import List

@dataclass
class User:
    user_id: int
    username: str
    password: str
    admin: bool

@dataclass
class Article:
    article_id: int
    title: str
    search_keys: str
    content: str

@dataclass
class AdviceTrigger:
    trigger_id: int
    lhs: str
    rhs: str
    logic: str
    article_id: int