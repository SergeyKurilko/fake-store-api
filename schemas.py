from pydantic import BaseModel, ConfigDict, Field

class ProductsByCategoryRequest(BaseModel):
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
    rating: dict


class ProductListByCategory(BaseModel):
    """Список продуктов по категории."""
    model_config = ConfigDict(from_attributes=True)
    items: list[ProductSchema]
    has_more: bool