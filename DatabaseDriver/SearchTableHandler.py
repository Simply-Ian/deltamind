class SearchTableHandler:

	def __init__(self, manager, model, forks_model):
		self.manager = manager
		self.model = model
		self.forks_model = forks_model

	async def handle(self, search_string: str):
		if search_string.isdigit():
			requested_map_query = await self.manager.execute(self.model.select().where(self.model.id==int(search_string)))
			requested_map = list(requested_map_query)
			if requested_map:
				return requested_map[0]
			else:
				return 'doesnt_exist'
		else:
			requested_maps_by_title_query = await self.manager.execute(self.model.select()
																.where(self.model.title.contains(search_string.lower())))
			requested_maps = list(requested_maps_by_title_query)

			requested_maps_by_nickname_query = await self.manager.execute(self.model.select().where((self.model.author_nickname==search_string)))
			requested_maps_by_nickname = list(requested_maps_by_nickname_query)

			requested_maps.extend(requested_maps_by_nickname)
			# Поиск форков не работал. Исправил и отладил
			additional_forks = []
			for req_map in requested_maps:
				forks_query = await self.__get_forks_if_exist(req_map.id)
				forks_raw = list(forks_query)
				if forks_raw:
					for fork in forks_raw:
						map_object = fork.fork
						map_object.title += f' fork of map #{fork.master_id} "{fork.master.title}"'
						additional_forks.append(map_object)
						requested_maps.remove([i for i in requested_maps if i.id == map_object.id][0])
			requested_maps.extend(additional_forks)
			if requested_maps:
				return requested_maps
			else:
				return 'doesnt_exist'

	async def __get_forks_if_exist(self, map_id):
		forks_subquery = await self.manager.execute(self.forks_model.select()
													.where((self.forks_model.master == map_id))
													.join(self.model, on=(self.forks_model.fork == self.model.id)))
		return forks_subquery
