class ShowInteractivesHandler:

	def __init__(self, manager, maps_model, inters_model):
		self.manager = manager
		self.maps_model = maps_model
		self.inters_model = inters_model

	async def handle(self, map_id, map_admin_password):
		requested_map_subquery = await self.manager.execute(self.maps_model.select()
														.where((self.maps_model.id==map_id)&(self.maps_model.admin_pass==map_admin_password)))
		if len(list(requested_map_subquery)) > 0:
			interactives_query = await self.manager.execute(self.inters_model.select()
															.where(self.inters_model.master_map==map_id)
															.order_by(self.inters_model.map_inner_ident))
			interactives = list(interactives_query)
			return interactives
		else:
			return 'doesnt_exist'

