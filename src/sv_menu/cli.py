import click
import datetime
from typing import Optional, List
from sv_menu.client import fetch_menus
from sv_menu.types import Menu
from sv_menu.cache_service import MenuCacheService
from sv_menu.ui import MenuUI

class MenuCLI:

    def __init__(self):
        self._cache = MenuCacheService(week_id=datetime.date.today().isocalendar()[1])
        self._ui = MenuUI()

    def _print_header(self, day: Optional[str]) -> None:
        click.echo("Welcome to the SV Menu CLI!")
        if day:
            click.echo(click.style(f"Displaying menu for {day}:", fg="green"))
        else:
            click.echo(click.style("Displaying menu for the current week:", fg="green"))
        click.echo("-" * 40)
        click.echo("⏳ Loading menus...")

    def _parse_day_to_date(self, day: str) -> Optional[datetime.date]:
        day = day.strip().lower()
        today = datetime.date.today()
        weekdays = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
        }

        if day == "today":
            return today
        elif day in weekdays:
            delta = weekdays[day] - today.weekday()
            return today + datetime.timedelta(days=delta)
        else:
            return None

    def _filter_menus_by_day(self, menus: List[Menu], day: str) -> List[Menu]:
        date = self._parse_day_to_date(day)
        if date is None:
            click.echo(click.style(
                f"Invalid day: {day}. Please use 'today', 'monday', 'tuesday', 'wednesday', 'thursday', or 'friday'.",
                fg="red"
            ))
            return []
        return [menu for menu in menus if menu.get("date") == date.isoformat()]

    def run(self, day: Optional[str] = None, no_cache: bool = False) -> None:
        self._print_header(day)

        self._cache.clear_caches()
        cached = self._cache.load_cache()
        if cached is not None and not no_cache:
            click.echo(click.style("Using cached menus.", fg="yellow"))
            menus = cached
        else:
            menus = fetch_menus()
            self._cache.save_cache(menus)

        if day:
            menus = self._filter_menus_by_day(menus, day)

        if not menus:
            click.echo(click.style("No menus available for this week / day.", fg="red"))
            return

        self._ui.render_week_menus(menus)


@click.command()
@click.option("--day", required=False, default=None, help="Day to display the menu for (optional).")
@click.option("--no-cache", is_flag=True, default=False, help="Ignore cache and fetch fresh data.")
def main(day: Optional[str] = None, no_cache: bool = False) -> None:
    """Displays week's menu in the terminal."""
    cli = MenuCLI()
    cli.run(day=day, no_cache=no_cache)
