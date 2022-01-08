import requests
import json

with open('/home/victor/PycharmProjects/schoolProject2021/SummerMindMap.deltamind', 'r') as FILE:
	map_code = FILE.read()
response = requests.post('http://127.0.0.1:8080/create_map', json=json.dumps({'map_title': 'map1',
															'author_nick': 'Ivan',
															'user_pass': '123456',
															'admin_pass': '123456789',
															'fork': -1,
															'map_code': map_code}))
print(response.text)