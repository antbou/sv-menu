from sqlite3 import Date
from typing import Dict, TypedDict, List

class Category(TypedDict):
    type: str
    title: str
    description: str
    priceInt: int
    priceExt: int

class Menu(TypedDict):
    id: str
    date: Date
    isHoliday: bool
    categories: List[Category]

Menus = List[Menu]

CATEGORY_ICONS: Dict[str, str] = {
    "Jardin": "🥦",
    "Menu": "🥩",
    "Marché": "🛒",
    "Soupe du jour": "🥣",
    "Sans titre": "🍽",
}
