import requests
response = requests.get('http://127.0.0.1:8000/3').json()
response = response[0][1]
print(response)