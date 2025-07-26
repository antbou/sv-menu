import click
from sv_menu.client import fetch_menus
from sv_menu.ui import render_week_menus


@click.command()
def main() -> None:
    """Displays week's menu in the terminal."""
    render_menu_for_week()


def render_menu_for_week() -> None:
    """Fetch and render the menu for the current work week (Monday to Friday)."""
    
    click.echo("⏳ Loading menus...")
    menus = fetch_menus()
    
    if not menus:
        click.echo(click.style("No menus available for this week.", fg="red"))
        return
    render_week_menus(menus)
