# import asyncio
# import requests
# from sqlalchemy.ext.asyncio import create_async_engine
# from config import settings
# from models import Base
#
# async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg,
#                        echo=True)
#
#
# async def create_db():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
# asyncio.run(create_db())

# посмотреть relationships + сделать логику работы с пользователями
# options(contains_eager(что подтянуть чтобы была вложенная структура)) подтяни если сможешь
# selectinload подтягивает джоины
# joinedload - one2one, many2one
# selectinload  - many2many, one2many
import requests
import json
params = {
    "grant_type": "",
    "username": "user1@example.com",
    "password": "string",
    "scope": "",
    "client_id": "",
    "client_secret": "",
}
headers = {
    "Content-Type": "application/json"
}
user = requests.request("POST", 'http://127.0.0.1:8000/auth/jwt/login?', json=json.dumps(params), headers=headers).cookies
print(user)
#делать авторизацию через jinja2+templates все таки в браузере :)
