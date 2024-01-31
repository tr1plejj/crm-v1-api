import requests
response = requests.post('http://127.0.0.1:8000/get_address/').json()
print(response[0][0])