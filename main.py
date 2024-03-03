from typing import List
import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import selectinload
from auth import User, Product, Offer, auth_backend, get_user_manager, UserRead, UserCreate, UserUpdate
from database import ProductOrm, async_session, OffersOrm, UserOrm
from sqlalchemy import select, desc, delete
from fastapi_users import FastAPIUsers

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.post('/put_in_db')
async def put_in_db(name: str, price: int, description: str):
    try:
        async with async_session() as session:
            product = ProductOrm(name=name, price=price, description=description)
            session.add(product)
            query = (
                select(ProductOrm.id).
                order_by(desc(ProductOrm.id)).
                limit(1)
            )
            prod_id = await session.execute(query)
            await session.commit()
            result = prod_id.scalars().one()
            return result
    except Exception as e:
        print(e)
    finally:
        await session.close()


@app.get('/take_from_db/{prod_id}', response_model=Product)
async def take_from_db(prod_id: int):
    try:
        async with async_session() as session:
            query = (
                select(ProductOrm).
                filter_by(id=prod_id)
            )
            product = await session.execute(query)
            product = product.scalars().one()
            return product
    except Exception as e:
        print(e)
    finally:
        await session.close()


@app.post('/put_address_in_db')
async def put_address_in_db(address: str, prod_id: int, user_id: int):
    try:
        async with async_session() as session:
            query = (
                select(ProductOrm.name).
                filter_by(id=prod_id)
            )
            name = await session.execute(query)
            name = name.scalars().one()
            offer = OffersOrm(name=name, prod_id=prod_id, address=address, user_id=user_id)
            session.add(offer)
            query = (
                select(OffersOrm.offer_id).
                order_by(desc(OffersOrm.offer_id)).
                limit(1)
            )
            of_id = await session.execute(query)
            await session.commit()
            of_id = of_id.scalars().one()
            return of_id
    except Exception as e:
        print(e)
    finally:
        await session.close()


@app.get('/get_offers_data', response_model=List[Offer])
async def get_offers_data():
    try:
        async with async_session() as session:
            query = (
                select(OffersOrm)
            )
            all_offers = await session.execute(query)
            return all_offers.scalars().all()
    except Exception as e:
        print(e)
    finally:
        await session.close()


@app.get('/get_offer_and_return/{id}')
async def get_offer_and_return(id: int):
    try:
        async with async_session() as session:
            query = (
                select(OffersOrm.user_id).
                filter_by(offer_id=id)
            )
            user_id = await session.execute(query)
            return user_id.scalars().one()
    except Exception as e:
        print(e)
    finally:
        await session.close()


@app.delete('/delete_from_offers_db/{id}')
async def delete_from_offers_db(id: int):
    try:
        async with async_session() as session:
            query = (
                delete(OffersOrm).
                filter_by(offer_id=id)
            )
            await session.execute(query)
            await session.commit()
            return {'status': 200}
    except Exception as e:
        print(e)
    finally:
        session.close()


@app.get('/all_users')
async def get_all_users():
    async with async_session() as session:
        query = (
            select(UserOrm)
            .options(selectinload(UserOrm.products))
            .options(selectinload(UserOrm.offers))
        )
        users = await session.execute(query)
        return users.unique().scalars().all()


if __name__ == '__main__':
    uvicorn.run(app)
