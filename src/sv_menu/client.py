import requests
from sv_menu.types import Menu

ENDPOINT_URL = "https://svm-o453.onrender.com/v1/api/menus"

def fetch_menus() -> list[Menu]:
    """Fetch menus from the API."""
    response = requests.get(ENDPOINT_URL)
    if response.status_code == 200:
        return response.json()
    return []