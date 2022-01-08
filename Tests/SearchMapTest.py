import requests

response = requests.get('http://127.0.0.1:8080/search_maps/Ivan1')
print(response.json())