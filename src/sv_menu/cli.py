import click
from sv_menu.scraper import fetch_menu_for_day
from datetime import datetime


@click.command()
@click.option("--day", default="today", help="Jour à afficher (e.g. today, monday, all)")
def main(day: str):
    """Affiche le menu du jour dans le terminal"""
    
    if day == "today":
        day = datetime.now().strftime("%Y-%m-%d")
    
    menu = fetch_menu_for_day(date=day)

    for section in menu:
        click.echo(click.style(f"\n## {section['category']}", fg="cyan"))
        for product in section["products"]:
            click.echo(f" - {product['name']}")
            if product["desc"]:
                click.echo(f"    {product['desc']}")
            for price in product["prices"]:
                click.echo(f"    {price}")
