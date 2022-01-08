from aiohttp import web
from Handlers import Handlers
import DatabaseDriver


app = web.Application()
handlers = Handlers(DatabaseDriver, app)
web.run_app(app, host='127.0.0.1', port=8080)