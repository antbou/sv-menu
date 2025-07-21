import click
from typing import Dict, List, Any

CATEGORY_ICONS = {
    "Jardin": "🥦",
    "Menu": "🥩",
    "Marché": "🛒",
    "Soupe du jour": "🥣",
    "Sans titre": "🍽",
}


def render_week_menu(week_data: Dict[str, List[Dict[str, Any]]]) -> None:
    for day, categories in week_data.items():
        click.echo()
        click.echo(click.style(f"📅 {day}", fg="yellow", bold=True))

        if not categories:
            click.echo(click.style("Restaurant fermé", fg="bright_black"))
            continue

        for category in categories:
            cat_name = category.get("category", "Sans titre")
            icon = CATEGORY_ICONS.get(cat_name, "🍽")
            click.echo(click.style(f"\n{icon} {cat_name}", bold=True))

            for product in category.get("products", []):
                name = product.get("name", "").strip()
                desc = product.get("desc", "").strip()
                prices = product.get("prices", [])

                line = click.style(f"  {name}", fg="bright_blue")
                if desc:
                    line += click.style(f" — {desc}", fg="bright_blue")
                click.echo(line)

                price_str = "   ".join(str(price) for price in prices)
                if price_str:
                    click.echo(click.style(f"    💵 {price_str} ", fg="bright_black", dim=True, italic=True))

        click.echo("-" * 40)
