from aiohttp import web
import json
import traceback


class Handlers:

	def __init__(self, db_driver, app: web.Application):
		self.master_app = app
		self.db_driver_package = db_driver
		self.setup_routes()

	def setup_routes(self):
		self.master_app.add_routes([web.post('/create_map', self.handle_map_creation),
									web.get('/get_map/{map_id}/{map_password}', self.handle_map_download),
									web.get('/search_maps/{search_string}', self.handle_map_search),
									web.get('/show_inters/{map_id}/{admin_password}', self.handle_show_interactives)])

	async def handle_map_creation(self, request):
		user_api_request = json.loads(await request.json())
		try:
			new_map_id = await self.db_driver_package.create_map(user_api_request['map_title'],
														   user_api_request['author_nick'],
														   user_api_request['user_pass'],
														   user_api_request['admin_pass'],
														   user_api_request['map_code'])
			if user_api_request['fork'] != -1:
				await self.db_driver_package.fork_map(user_api_request['fork'], new_map_id)
			return web.Response(text=str(new_map_id))
		except KeyError:
			raise web.HTTPBadRequest(reason='wrong_json_key')

	async def handle_map_download(self, request):
		user_api_request = request.match_info
		try:
			if 'map_password' in user_api_request.keys():
				password = user_api_request['map_password']
			else:
				raise web.HTTPBadRequest(reason='no_password_field')
			requested_map = await self.db_driver_package.download_map(user_api_request['map_id'], password)
			if requested_map == 'wrong_password':
				raise web.HTTPForbidden(reason='Wrong Password')
			elif requested_map == 'doesnt_exist':
				raise web.HTTPNotFound(reason='There is no map with such id')
			else:
				return web.json_response({'map_id': requested_map.id,
										  'title': requested_map.title,
										  'author_nick': requested_map.author_nickname,
										  'creating_date': requested_map.creating_date.strftime('%d-%m-%Y'),
										  'map_code': ';\n'.join(requested_map.map_code)})
		except Exception as e:
			raise web.HTTPServerError(reason=traceback.format_exc())

	async def handle_map_search(self, request):
		user_api_request = request.match_info
		try:
			if 'search_string' in user_api_request.keys():
				requested_maps = await self.db_driver_package.search_map(user_api_request['search_string'])
				if requested_maps == 'doesnt_exist':
					raise web.HTTPNotFound(reason='There is no map with such id or title.')
				if not isinstance(requested_maps, list):
					requested_maps = [requested_maps]
				return web.json_response({'maps': [{'map_id': i.id,
									  'title': i.title,
									  'author_nick': i.author_nickname,
									  'creating_date': i.creating_date.strftime('%d-%m-%Y')} for i in requested_maps]})
		except Exception as e:
			raise web.HTTPServerError(reason=traceback.format_exc())

	async def handle_show_interactives(self, request):
		user_api_request = request.match_info
		try:
			requested_interactives = await self.db_driver_package.show_interactives(user_api_request['map_id'],
																					user_api_request['admin_password'])
			return web.json_response([{'id': i.map_inner_ident,
									   'inter_type': i.interactive_type,
									   'text': i.text_hint,
									   'value': i.value,
									   'combo_items': i.combo_items} for i in requested_interactives])
		except KeyError:
			raise web.HTTPBadRequest(reason='wrong_json_key')
