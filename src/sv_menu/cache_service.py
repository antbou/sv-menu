import json
import time
from typing import Optional, List
import click
from sv_menu.types import Menu
from pathlib import Path


CACHE_EXPIRATION_TIME = 60 * 60 * 24 * 2
MIN_MENUS_FOR_CACHE = 3
FILE_NAME = "sv-menu_cache"
DIR_NAME = ".cache"

class MenuCacheService:
    def __init__(self, week_id: int):
        self.cache_file = Path.home() / DIR_NAME / f"{FILE_NAME}_{week_id}.json"
        self.ttl = CACHE_EXPIRATION_TIME

    def load_cache(self) -> Optional[List[Menu]]:
        """Load cached menus if available and not expired."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                cache_time = cache.get("timestamp", 0)
                if time.time() - cache_time < self.ttl and "menus" in cache:
                    return cache["menus"]
            except (FileNotFoundError, json.JSONDecodeError, OSError):
                pass
        return None
    
    def clear_caches(self) -> None:
        """Clear all cache files."""
        path = Path.home() / DIR_NAME
        if not path.exists():
            return
        for file in path.glob(f"{FILE_NAME}_*.json"):
            try:
                click.echo(f"Removing cache file: {file.name}")
                if file.name == self.cache_file.name:
                    continue
                file.unlink()
            except OSError:
                pass
        

    def save_cache(self, menus: List[Menu]) -> None:
        """Save menus to cache if they meet the minimum requirement."""
        if not menus or len(menus) < MIN_MENUS_FOR_CACHE:
            return
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump({"timestamp": time.time(), "menus": menus}, f)
        except (OSError, TypeError):
            pass
