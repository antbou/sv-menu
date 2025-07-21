from typing import TypedDict, List, Dict

class Product(TypedDict):
    name: str
    desc: str
    prices: List[str]

class CategoryBlock(TypedDict):
    category: str
    products: List[Product]

WeekMenu = Dict[str, List[CategoryBlock]]
