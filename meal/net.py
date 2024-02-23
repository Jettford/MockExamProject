import hashlib
import os
import requests

from typing import Optional

class Net
    @staticmethod
    def run_checks() -> None:
        if not os.path.exists("cache"):
            os.mkdir("cache")

    @staticmethod
    def cache_route(method: str, uri: str, res: str) -> None:
        hashingStr = method + uri
        hashedStr = hashlib.md5(hashingStr.encode("utf-8"))

        with open("cached/" + hashedStr) as f:
            f.write(res)

    @staticmethod
    def check_route(method: str, uri: str) -> Optional[str]:
        if os.path.exists("cached/" + hashlib.md5((method + uri).encode())):
            with open("cached/" + hashlib.md5((method + uri).encode())) as f:
                return f.read()
            
        return None


    @staticmethod
    def get(uri: str) -> str:
        Net.run_checks()

        check = Net.check_route("GET", uri)

        if check:
            return check

        value = requests.get(uri)

        Net.cache_route("GET", uri, value.text)

        return value.text
