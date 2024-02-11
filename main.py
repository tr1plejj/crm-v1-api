from fastapi import FastAPI
import uvicorn
import psycopg2
import requests

host = db_host
user = db_user
password = db_pass
db_name = db_name


app = FastAPI()


@app.post('/put_in_db')
def put_in_db(name: str, price: str, description: str):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(f"insert into prod_data(name, price, description) values ('{name}', '{price}', '{description}')")
            cursor.execute("select id from prod_data order by id desc limit 1")
            last_id = cursor.fetchone()
        connection.commit()
        return last_id
    except Exception as _ex:
        print('[INFO]', _ex)

    finally:
        if connection:
            connection.close()

@app.get('/take_from_db/{id}')
def take_from_db(id: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(f"select name, price, description, id from prod_data where id = {id}")
            about_prod = cursor.fetchall()
        connection.commit()
        return about_prod
    except Exception as _ex:
        print('[INFO]', _ex)
    finally:
        if connection:
            connection.close()


@app.post('/put_address_in_db')
def put_address_in_db(address: str, prod_id: int, user_id: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            data = requests.get(f'http://127.0.0.1:8000/take_from_db/{prod_id}').json()
            name = str(data[0][0])
            print(name, prod_id, address)
            cursor.execute(f"insert into offers_data(name, address, prod_id, user_id) values ('{name}', '{address}', '{prod_id}', '{user_id}')")
            cursor.execute("select offer_id from offers_data order by offer_id desc limit 1")
            offer_id = cursor.fetchone()
        connection.commit()
        return offer_id
    except Exception as _ex:
        print('[INFO]', _ex)

    finally:
        if connection:
            connection.close()


@app.get('/get_offers_data')
def get_offers_data():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute("select * from offers_data")
            all_data = cursor.fetchall()
        connection.commit()
        return all_data
    except Exception as _ex:
        print('[INFO]', _ex)
    finally:
        if connection:
            connection.close()

@app.get('/get_offer_and_return/{id}')
def get_offer_and_return(id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(f"select user_id from offers_data where offer_id = {id}")
            all_id = cursor.fetchone()
        connection.commit()
        return all_id
    except Exception as _ex:
        print('[INFO]', _ex)
    finally:
        if connection:
            connection.close()

@app.delete('/delete_from_offers_db/{id}')
def delete_from_offers_db(id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(f"delete from offers_data where offer_id = {id}")
        connection.commit()
    except Exception as _ex:
        print('[INFO]', _ex)
    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    uvicorn.run(app)

