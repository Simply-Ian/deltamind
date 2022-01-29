from aiohttp import web
from Handlers import Handlers
import DatabaseDriver
import json
import os

with open('config.json', 'r') as FILE:
	config_dict = json.load(FILE)
app = web.Application()
handlers = Handlers(DatabaseDriver, app)
web.run_app(app, host=config_dict['hostname'] or None, port=int(os.environ['PORT']))