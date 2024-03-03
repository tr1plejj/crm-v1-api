from typing import List
from fastapi import FastAPI
import uvicorn
from models import ProductOrm, async_session, OffersOrm, Product, Offers
from sqlalchemy import select, desc, delete

app = FastAPI()


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


@app.get('/get_offers_data', response_model=List[Offers])
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
            user = await session.execute(query)
            return user.scalars().one()
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

if __name__ == '__main__':
    uvicorn.run(app)

