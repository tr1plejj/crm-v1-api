import requests
response = requests.get('http://127.0.0.1:8000/take_from_db/12').json()
print(response[0][0])