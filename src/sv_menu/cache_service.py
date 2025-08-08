import json
import time
from typing import List, Sequence
import click
from sv_menu.types import Menu
from pathlib import Path


CACHE_EXPIRATION_TIME = 60 * 60 * 24 * 2
MIN_MENUS_FOR_CACHE = 3
FILE_NAME = "sv-menu_cache"
DIR_NAME = ".cache"
ERROR_LOG_FILE = Path.home() / DIR_NAME / "sv-menu_cache_errors.log"

class MenuCacheService:
    _cache_dir = Path.home() / DIR_NAME

    def __init__(self, week_id: int):
        self.cache_file = self._cache_dir / f"{FILE_NAME}_{week_id}.json"
        self.ttl = CACHE_EXPIRATION_TIME

    def _log_error(self, message: str) -> None:
        try:
            ERROR_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(ERROR_LOG_FILE, "a", encoding="utf-8") as logf:
                logf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
        except Exception:
            pass

    def load_cache(self) -> List[Menu]:
        """Load cached menus if available and not expired."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                cache_time = cache.get("timestamp", 0)
                if time.time() - cache_time < self.ttl and "menus" in cache:
                    click.echo(click.style("Using cached menus.", fg="yellow"))
                    return cache["menus"]
            except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
                self._log_error(f"Error loading cache: {e}")
        return []
    
    def clear_caches(self, all: bool = False) -> None:
        """Clear all cache files. If 'all' is False, keep the current cache file."""
        path = self._cache_dir
        if not path.exists():
            return
        for file in path.glob(f"{FILE_NAME}_*.json"):
            try:
                if not all and file.name == self.cache_file.name:
                    continue
                if file.name == self.cache_file.name:
                    click.echo(click.style(f"Deleting current cache file: {file.name}", fg="yellow"))
                    
                file.unlink()
            except OSError as e:
                self._log_error(f"Error removing cache file {file}: {e}")
        

    def save_cache(self, menus: Sequence[Menu]) -> None:
        """Save menus to cache if they meet the minimum requirement."""
        if not menus or len(menus) < MIN_MENUS_FOR_CACHE:
            return
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump({"timestamp": time.time(), "menus": menus}, f)
        except (OSError, TypeError) as e:
            self._log_error(f"Error saving cache: {e}")
