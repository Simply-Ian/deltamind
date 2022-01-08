import requests

response = requests.get('http://127.0.0.1:8080/get_map/2/123456')
print(response.json())