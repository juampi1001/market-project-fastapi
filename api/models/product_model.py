from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema
from enum import Enum

class Category(str, Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    HOME_FURNITURE = "home_furniture"
    BEAUTY_HEALTH = "beauty_health"
    SPORTS_OUTDOORS = "sports_outdoors"
    TOYS_HOBBIES = "toys_hobbies"
    FOOD_GROCERIES = "food_groceries"
    AUTOMOTIVE = "automotive"
    BABY_KIDS = "baby_kids"
    OFFICE_SUPPLIES = "office_supplies"
    OTHERS = "others"

class Product(BaseModel):
    id: SkipJsonSchema[str] = None
    name: str
    images: List[str]
    description: str
    price: float
    final_price: SkipJsonSchema[float] = None
    discount: Optional[float]
    quantity: int
    category: Category
    tags: Optional[List[str]] = None 
    creation_datetime: SkipJsonSchema[str] = None
    modification_datetime: SkipJsonSchema[str] = None