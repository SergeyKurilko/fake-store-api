from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_db
from database.models import FakeProduct
from schemas import FakeProductSchema
from services import products_services as ps
from settings import BEARER_TOKEN


security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Асинхронная проверка токена"""
    token = credentials.credentials
    if token != BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )
    return token

router = APIRouter(dependencies=[Depends(verify_token)])

@router.get("/products/{product_id}")
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_db)):
    product: FakeProduct | None = await ps.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return FakeProductSchema.model_validate(product)