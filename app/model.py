from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    description: str
    img_url: str
    type: str


class Comment(BaseModel):
    name: str
    content: str
    instrument_id: str
    created_at: str


class Instrument(BaseModel):
    id: str
    name: str
    price: int
    description: str
    material: str
    category_id: str
    img_url: str
    rating: int
    is_in_the_shop: bool = True
