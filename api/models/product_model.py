from typing import Optional
from pydantic import BaseModel
from pydantic.json_schema import SkipJsonSchema

class Product(BaseModel):
    id: SkipJsonSchema[str] = None
    name: str
    description: str
    price: float
    final_price: SkipJsonSchema[float] = None
    discount: Optional[float]
    quantity: int
    creation_datetime: SkipJsonSchema[str] = None
    modification_datetime: SkipJsonSchema[str] = None