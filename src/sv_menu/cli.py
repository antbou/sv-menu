import click
from datetime import datetime, timedelta
from typing import Optional
from sv_menu.scraper import fetch_menus_for_days
from sv_menu.ui import render_week_menu
from sv_menu.types import WeekMenu


@click.command()
@click.option(
    "--date",
    help="Date au format YYYY-MM-DD pour un jour spécifique. Par défaut, affiche toute la semaine.",
    required=False
)
def main(date: Optional[str]) -> None:
    """Displays today's or the week's menu in the terminal."""
    if date:
        render_menu_for_date(date)
    else:
        render_menu_for_week()


def render_menu_for_date(date_str: str) -> None:
    """Fetch and render the menu for a specific date."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise click.ClickException("Format de date invalide. Utilise YYYY-MM-DD.")

    menus = fetch_menus_for_days([date_str])
    label = date_obj.strftime("%A").capitalize()  # e.g., "Monday"
    typed = menus.get(date_str, [])

    render_week_menu({label: typed})


def render_menu_for_week() -> None:
    """Fetch and render the menu for the current work week (Monday to Friday)."""
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())  # Get Monday of current week

    # Generate list of dates from Monday to Friday
    week_dates = [(monday + timedelta(days=i)) for i in range(5)]
    iso_dates = [d.strftime("%Y-%m-%d") for d in week_dates]

    menus_by_date = fetch_menus_for_days(iso_dates)

    # Map ISO date to day name
    menus_by_day: WeekMenu = {
    d.strftime("%A").capitalize(): menus_by_date.get(d.strftime("%Y-%m-%d"), [])
    for d in week_dates
}

    # Remove empty days (e.g., holidays or closed)
    menus_by_day = {k: v for k, v in menus_by_day.items() if v}

    render_week_menu(menus_by_day)
