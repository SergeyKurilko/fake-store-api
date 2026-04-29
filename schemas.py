from pydantic import BaseModel, ConfigDict, Field

class RatingSchema(BaseModel):
    """Схема объекта rating в объекте ProductSchema"""
    rate: float
    count: int

class ProductsByCategoryRequest(BaseModel):
    """Запрос списка продуктов по категории"""
    category_id: int = Field(gt=0)
    page: int  = Field(default=1, ge=1)
    limit: int  = Field(default=20, ge=1, le=20)


class ProductSchema(BaseModel):
    """Продукт"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    price: int
    description: str
    category_id: int
    image: str
    rating: RatingSchema


class ProductListByCategory(BaseModel):
    """Список продуктов по категории."""
    model_config = ConfigDict(from_attributes=True)
    items: list[ProductSchema]
    has_more: bool