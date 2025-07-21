from playwright.sync_api import sync_playwright
from typing import List, Dict, Any

ENDPOINT_URL = "https://www.sv-restaurant.ch/menu/La%20Mobili%C3%A8re,%20Nyon/Menu%20de%20midi"

def fetch_menus_for_days(dates: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """Récupère les menus pour plusieurs dates avec une seule session Playwright."""
    results: Dict[str, List[Dict[str, Any]]] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for date in dates:
            target_url = f"{ENDPOINT_URL}/date/{date}"
            page.goto(target_url)
            try:
                page.wait_for_selector(".category-grid", timeout=5000)
            except Exception:
                results[date] = []
                continue

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
                        "prices": [p.inner_text().strip() for p in prices],
                    })

                menu.append({
                    "category": title,
                    "products": products,
                })

            results[date] = menu

        browser.close()

    return results
