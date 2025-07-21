from playwright.sync_api import sync_playwright
from typing import List, Dict, Any

ENDPOINT_URL: str = "https://www.sv-restaurant.ch/menu/La%20Mobili%C3%A8re,%20Nyon/Menu%20de%20midi" 

def fetch_menu_for_day(date: str) -> List[Dict[str, Any]]:
    """Fetches the menu for a specific date from the restaurant's website."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        target_url = f"{ENDPOINT_URL}/date/{date}"
        page.goto(target_url)

        page.wait_for_selector(".category-grid")
        categories = page.query_selector_all(".grid-row")

        menu: List[Dict[str, Any]] = []

        for cat in categories:
            title_el = cat.query_selector("h3.category-header")
            title = title_el.inner_text().strip() if title_el else "Sans titre"

            products: List[Dict[str, Any]] = []
            for product in cat.query_selector_all(".product-wrapper"):
                name = product.query_selector(".legacy-text-xxl")
                description = product.query_selector(".product-teaser")
                prices = product.query_selector_all(".price")

                products.append({
                    "name": name.inner_text().strip() if name else "",
                    "desc": description.inner_text().strip() if description else "",
                    "prices": [p.inner_text().strip() for p in prices]
                })

            menu.append({
                "category": title,
                "products": products
            })

        browser.close()
        return menu