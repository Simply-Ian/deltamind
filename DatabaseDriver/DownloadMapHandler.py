class DownloadMapHandler:

	def __init__(self, manager, model):
		self.manager = manager
		self.model = model

	async def handle(self, requested_map_id, password):
		requested_map_query = await self.manager.execute(self.model.select().where(self.model.id==requested_map_id))
		requested_maps = list(requested_map_query)
		if requested_maps:
			requested_map = requested_maps[0]
			if password in (requested_map.admin_pass, requested_map.user_pass):
				return requested_map
			else:
				return 'wrong_password'
		else:
			return 'doesnt_exist'