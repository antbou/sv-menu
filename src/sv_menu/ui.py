import click
from datetime import datetime
from sv_menu.types import CATEGORY_ICONS, Menu, Category

class MenuUI:
    # French weekday names
    FRENCH_WEEKDAYS = {
        0: "Lundi",
        1: "Mardi",
        2: "Mercredi",
        3: "Jeudi",
        4: "Vendredi",
        5: "Samedi",
        6: "Dimanche"
    }

    def _format_date_with_weekday(self, date_str: str) -> str:
        """Format date string to include French weekday name."""
        try:
            date_obj = datetime.fromisoformat(date_str).date()
            weekday_name = self.FRENCH_WEEKDAYS.get(date_obj.weekday(), "")
            return f"{weekday_name} {date_str}"
        except (ValueError, AttributeError):
            return date_str

    def render_week_menus(self, menus: list[Menu]) -> None:
        """Render the menus for the week."""
        for menu in menus:
            date = menu.get("date", "Inconnu")
            formatted_date = self._format_date_with_weekday(date)
            click.echo(click.style(f"📅 {formatted_date}", fg="yellow", bold=True))

            categories = menu.get("categories", [])
            if not categories or menu.get("isHoliday", False):
                click.echo(click.style("Restaurant fermé ou pas de menu disponible.", fg="red"))
                click.echo("-" * 40)
                continue

            for category in categories:
                self._render_category(category)

            click.echo("-" * 40)

    def _render_category(self, cat: Category) -> None:
        """Render a single category."""
        name = cat.get("type", "Sans titre")
        icon = CATEGORY_ICONS.get(name, CATEGORY_ICONS["Sans titre"])
        click.echo(click.style(f"{icon} {name}", bold=True))

        title = cat.get("title", "").strip()
        description = cat.get("description", "").strip()
        priceInt = cat.get("priceInt", 0)
        priceExt = cat.get("priceExt", 0)

        line = click.style(f"  {title}", fg="bright_blue")
        if description:
            line += click.style(f" — {description}", fg="bright_blue")
        click.echo(line)

        if priceInt or priceExt:
            price_str = f"💵 {priceInt} / {priceExt}"
            click.echo(click.style(f"    {price_str}", fg="bright_black", dim=True, italic=True))
