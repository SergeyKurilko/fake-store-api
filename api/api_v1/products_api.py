from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_db
from database.models import FakeProduct
from schemas import FakeProductSchema
from services import products_services as ps

router = APIRouter()

@router.get("/products/{product_id}")
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_db)):
    product: FakeProduct | None = await ps.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return FakeProductSchema.model_validate(product)