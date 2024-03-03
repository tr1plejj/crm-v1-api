from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from database import settings
from pydantic import BaseModel

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


class ProductOrm(Base):
    __tablename__ = "product_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]


class OffersOrm(Base):
    __tablename__ = "offer_data"
    name: Mapped[str]
    prod_id: Mapped[int]
    address: Mapped[str]
    offer_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]


class Product(BaseModel):
    id: int
    name: str
    price: int
    description: str


class Offers(BaseModel):
    name: str
    prod_id: int
    address: str
    offer_id: int
    user_id: int


