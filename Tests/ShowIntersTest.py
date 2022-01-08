import requests

response = requests.get('http://127.0.0.1:8080/show_inters/4/123456789')
print(response.json())