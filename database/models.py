from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import JSON


class Base(DeclarativeBase):
    pass


class FakeProduct(Base):
    __tablename__ = 'fake_products'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[dict] = mapped_column(JSON, nullable=False)
