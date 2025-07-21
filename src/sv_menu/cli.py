import click
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List

from sv_menu.scraper import fetch_menus_for_days
from sv_menu.ui import render_week_menu


@click.command()
@click.option(
    "--date",
    help="Date au format YYYY-MM-DD pour un jour spécifique. Par défaut, affiche toute la semaine.",
    required=False
)
def main(date: Optional[str]) -> None:
    """Affiche le menu du jour ou de la semaine dans le terminal."""

    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise click.ClickException("Format de date invalide. Utilise YYYY-MM-DD.")

        menus = fetch_menus_for_days([date])
        label = date_obj.strftime("%A").capitalize()
        render_week_menu({label: menus[date]})

    else:
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())  # Go back to Monday

        dates = [(monday + timedelta(days=i)) for i in range(5)]
        iso_dates = [d.strftime("%Y-%m-%d") for d in dates]
        menus_by_date = fetch_menus_for_days(iso_dates)
        click.echo(menus_by_date)
        menus_by_day: Dict[str, List[Any]] = {
            d.strftime("%A").capitalize(): menus_by_date[d.strftime("%Y-%m-%d")]
            for d in dates
        }
        menus_by_day = {k: v for k, v in menus_by_day.items() if v}

        render_week_menu(menus_by_day)
