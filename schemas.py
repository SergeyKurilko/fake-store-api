from pydantic import BaseModel, ConfigDict


class FakeProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: int
    description: str
    category: str
    image: str
    rating: dict
