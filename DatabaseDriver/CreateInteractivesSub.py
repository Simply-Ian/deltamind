import json


async def create_interactives(map_objects, manager, inter_model, new_map_id):
	for serialized_obj in map_objects:
		obj_ = json.loads(serialized_obj)
		if obj_['class'] == 'Interactive':
			if obj_['inter_type'] == 'CT':
				combo_items = obj_['pet_items']
			else:
				combo_items = []
			await manager.create(inter_model, master_map=new_map_id,
									  value=obj_['value'],
									  text_hint=obj_['text'],
									  combo_items=combo_items,
									  map_inner_ident=obj_['id'],
									  interactive_type=obj_['inter_type'][0])