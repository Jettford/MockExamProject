import os
import json
import hashlib
import requests

class Net:
    @staticmethod
    def verify_cache():
        if not os.path.exists("cache"):
            os.mkdir("cache")

    @staticmethod
    def cache_exists(url: str):
        return os.path.exists(f"cache/{hashlib.sha256(url.encode()).hexdigest()}")

    @staticmethod
    def request_resource(url: str):
        if not Net.cache_exists(url):
            Net.verify_cache()

            with open(f"cache/{hashlib.sha256(url.encode()).hexdigest()}", "w") as f:
                f.write(requests.get(url).text)

        return open(f"cache/{hashlib.sha256(url.encode()).hexdigest()}", "r").read()
    
    @staticmethod
    def request_json_resource(url: str):
        return json.loads(Net.request_resource(url))