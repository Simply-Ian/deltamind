import datetime
from DatabaseDriver.CreateInteractivesSub import create_interactives


class CreateMapHandler:

	def __init__(self, manager, model, inter_model):
		self.manager = manager
		self.model = model
		self.inter_model = inter_model

	async def handle(self, title: str, author_nick: str, user_pass: str, admin_pass: str, map_code: str):
		map_objects = [i for i in map_code.split(';\n') if i]
		new_map = await self.manager.create(self.model, title=title,
								author_nickname=author_nick,
								creating_date=datetime.datetime.now().date(),
								user_pass=user_pass,
								admin_pass=admin_pass,
								map_code=map_objects)
		await create_interactives(map_objects, self.manager, self.inter_model, new_map.id)
		return new_map.id