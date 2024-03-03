from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from database import settings


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


class UserOrm(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    products: Mapped[list["ProductOrm"]] = relationship(
        back_populates="user",
        primaryjoin="UserOrm.id == ProductOrm.user_id"
    )
    offers: Mapped[list["OffersOrm"]] = relationship(
        back_populates="user",
        primaryjoin="UserOrm.id == OffersOrm.user_id"
    )


class ProductOrm(Base):
    __tablename__ = "product_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["UserOrm"] = relationship(
        back_populates="products"
    )


class OffersOrm(Base):
    __tablename__ = "offer_data"
    name: Mapped[str]
    prod_id: Mapped[int]
    address: Mapped[str]
    offer_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["UserOrm"] = relationship(
        back_populates="offers"
    )
