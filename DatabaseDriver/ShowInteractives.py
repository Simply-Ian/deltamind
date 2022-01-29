class ShowInteractivesHandler:

	def __init__(self, manager, maps_model, inters_model, forks_model):
		self.manager = manager
		self.maps_model = maps_model
		self.inters_model = inters_model
		self.forks_model = forks_model

	async def handle(self, map_id, map_admin_password):
		requested_map_subquery = await self.manager.execute(self.maps_model.select()
														.where((self.maps_model.id==map_id)
															   &(self.maps_model.admin_pass==map_admin_password)))
		if len(list(requested_map_subquery)) > 0:
			requested_map = list(requested_map_subquery)[0]
			additional_forks_subquery = await self.__get_forks_if_exist(map_id)
			additional_forks = [i.fork for i in list(additional_forks_subquery)]
			maps_to_look_up = additional_forks + [requested_map]
			for_return = []
			for map_ in maps_to_look_up:
				cur_map_inters = []
				interactives_query = await self.manager.execute(self.inters_model.select()
																.where(self.inters_model.master_map==map_.id)
																.order_by(self.inters_model.map_inner_ident))
				inters_list = list(interactives_query)
				for inter_elem in inters_list:
					cur_map_inters.append({'map_id': map_.id,
									   'map_author_nick': map_.author_nickname,
									   'map_date': map_.creating_date.strftime('%d-%m-%Y'),
									   'id': inter_elem.map_inner_ident,
										'inter_type': inter_elem.interactive_type,
										'text': inter_elem.text_hint,
										'value': inter_elem.value,
										'combo_items': inter_elem.combo_items})
				for_return.append(cur_map_inters)
			return for_return
		else:
			return 'doesnt_exist'

	async def __get_forks_if_exist(self, map_id):
		forks_subquery = await self.manager.execute(self.forks_model.select()
													.where((self.forks_model.master == map_id))
													.join(self.maps_model, on=(self.forks_model.fork == self.maps_model.id)))
		return forks_subquery

