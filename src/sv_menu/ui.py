import click
from typing import Dict
from sv_menu.types import WeekMenu, CategoryBlock, Product

CATEGORY_ICONS: Dict[str, str] = {
    "Jardin": "🥦",
    "Menu": "🥩",
    "Marché": "🛒",
    "Soupe du jour": "🥣",
    "Sans titre": "🍽",
}

DEFAULT_ICON = "🍽"


def render_week_menu(week_data: WeekMenu) -> None:
    for day, categories in week_data.items():
        click.echo()
        _render_day_header(day)

        if not categories:
            click.echo(click.style("Restaurant fermé", fg="bright_black"))
            continue

        for category in categories:
            _render_category(category)

        click.echo("-" * 40)


def _render_day_header(day: str) -> None:
    click.echo(click.style(f"📅 {day}", fg="yellow", bold=True))


def _render_category(cat: CategoryBlock) -> None:
    name = cat.get("category", "Sans titre")
    icon = CATEGORY_ICONS.get(name, DEFAULT_ICON)
    click.echo(click.style(f"\n{icon} {name}", bold=True))

    for product in cat.get("products", []):
        _render_product(product)


def _render_product(product: Product) -> None:
    name = product.get("name", "").strip()
    desc = product.get("desc", "").strip()
    prices = product.get("prices", [])

    line = click.style(f"  {name}", fg="bright_blue")
    if desc:
        line += click.style(f" — {desc}", fg="bright_blue")
    click.echo(line)

    if prices:
        price_str = "   ".join(prices)
        click.echo(click.style(f"    💵 {price_str}", fg="bright_black", dim=True, italic=True))
