import click
import requests
import urllib3
from sv_menu.types import Menu

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ENDPOINT_URL = "https://svm-menu.fly.dev/v1/api/menus"

def fetch_menus() -> list[Menu]:
    """Fetch menus from the API."""
    click.echo(click.style("Fetching menus from the API...", fg="yellow"))
    response = requests.get(ENDPOINT_URL, headers={"Accept": "application/json"}, verify=False)
    if response.status_code == 200:
        menus = response.json()
        return menus
    return []