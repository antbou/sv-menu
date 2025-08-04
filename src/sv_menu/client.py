
import certifi
import requests
from sv_menu.types import Menu
from sv_menu.cache_service import MenuCacheService

ENDPOINT_URL = "https://svm-menu.fly.dev/v1/api/menus"
_cache = MenuCacheService()

def fetch_menus() -> list[Menu]:
    """Fetch menus from the API, with weekly cache (via MenuCacheService)."""
    cached = _cache.load_cache()
    if cached is not None:
        return cached

    response = requests.get(ENDPOINT_URL, headers={"Accept": "application/json"}, verify=certifi.where())
    if response.status_code == 200:
        menus = response.json()
        _cache.save_cache(menus)
        return menus
    return []