import click
from sv_menu.types import CATEGORY_ICONS, Menu, Category

def render_week_menus(menus: list[Menu]) -> None:
    for menu in menus:
        date = menu.get("date", "Inconnu")
        click.echo(click.style(f"📅 {date}", fg="yellow", bold=True))

        categories = menu.get("categories", [])
        if not categories or menu.get("isHoliday", False):
            click.echo(click.style("Restaurant fermé ou pas de menu disponible.", fg="red"))
            click.echo("-" * 40)
            continue

        for category in categories:
            _render_category(category)

        click.echo("-" * 40)

def _render_category(cat: Category) -> None:
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
