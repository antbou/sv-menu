from typing import List
from playwright.sync_api import sync_playwright, TimeoutError
from sv_menu.types import WeekMenu, CategoryBlock, Product
from playwright.sync_api import Page


ENDPOINT_URL = "https://www.sv-restaurant.ch/menu/La%20Mobili%C3%A8re,%20Nyon/Menu%20de%20midi"
SELECTOR = ".category-grid"
TIMEOUT_MS = 5000

def fetch_menus_for_days(dates: List[str]) -> WeekMenu:
    """Fetches and parses the menu for multiple dates using Playwright."""
    results: WeekMenu = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for date in dates:
            url = f"{ENDPOINT_URL}/date/{date}"
            page.goto(url)

            try:
                page.wait_for_selector(SELECTOR, timeout=TIMEOUT_MS)
            except TimeoutError:
                results[date] = []
                continue

            results[date] = _parse_menu_page(page)

        browser.close()

    return results

def _parse_menu_page(page: Page) -> List[CategoryBlock]:
    """Parses the menu page and returns structured data."""
    categories = page.query_selector_all(".grid-row")
    menu: List[CategoryBlock] = []

    for cat in categories:
        title_el = cat.query_selector("h3.category-header")
        title = title_el.inner_text().strip() if title_el else "Sans titre"

        products: List[Product] = []
        for product in cat.query_selector_all(".product-wrapper"):
            name_el = product.query_selector(".legacy-text-xxl")
            desc_el = product.query_selector(".product-teaser")
            prices_els = product.query_selector_all(".price")

            products.append({
                "name": name_el.inner_text().strip() if name_el else "",
                "desc": desc_el.inner_text().strip() if desc_el else "",
                "prices": [p.inner_text().strip() for p in prices_els]
            })

        menu.append({
            "category": title,
            "products": products
        })

    return menu
