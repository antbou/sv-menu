
import json
import os
import time
from typing import Optional, List
from sv_menu.types import Menu

class MenuCacheService:
    def __init__(self, cache_file: str = "menus_cache.json", ttl: int = 60 * 60 * 24 * 7):
        self.cache_file = cache_file
        self.ttl = ttl

    def load_cache(self) -> Optional[List[Menu]]:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                cache_time = cache.get("timestamp", 0)
                if time.time() - cache_time < self.ttl and "menus" in cache:
                    return cache["menus"]
            except Exception:
                pass
        return None

    def save_cache(self, menus: List[Menu]) -> None:
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump({"timestamp": time.time(), "menus": menus}, f)
        except Exception:
            pass
