import click
import datetime
from typing import Optional, List
from sv_menu.client import fetch_menus
from sv_menu.types import Menu
from sv_menu.ui import render_week_menus
from sv_menu.cache_service import MenuCacheService

_cache = MenuCacheService()

def print_header(day: Optional[str]) -> None:
    click.echo("Welcome to the SV Menu CLI!")
    if day:
        click.echo(click.style(f"Displaying menu for {day}:", fg="green"))
    else:
        click.echo(click.style("Displaying menu for the current week:", fg="green"))
    click.echo("-" * 40)
    click.echo("⏳ Loading menus...")


def parse_day_to_date(day: str) -> Optional[datetime.date]:
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


def filter_menus_by_day(menus: List[Menu], day: str) -> List[Menu]:
    date = parse_day_to_date(day)
    if date is None:
        click.echo(click.style(
            f"Invalid day: {day}. Please use 'today', 'monday', 'tuesday', 'wednesday', 'thursday', or 'friday'.",
            fg="red"
        ))
        return []
    return [menu for menu in menus if menu.get("date") == date.isoformat()]


@click.command()
@click.option("--day", required=False, default=None, help="Day to display the menu for (optional).")
@click.option("--no-cache", is_flag=True, default=False, help="Ignore cache and fetch fresh data.")
def main(day: Optional[str] = None, no_cache: bool = False) -> None:
    """Displays week's menu in the terminal."""
    print_header(day)

    cached = _cache.load_cache()
    if cached is not None and not no_cache:
        click.echo(click.style("Using cached menus.", fg="yellow"))
        menus = cached
    else:
        menus = fetch_menus()
        if len(menus) >= 3:
            _cache.save_cache(menus)

    if day:
        menus = filter_menus_by_day(menus, day)

    if not menus:
        click.echo(click.style("No menus available for this week / day.", fg="red"))
        return

    render_week_menus(menus)
