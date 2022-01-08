from DatabaseDriver.Models import database, Interactives, Maps, Forks
from peewee_async import Manager
from DatabaseDriver.CreateMapHandler import CreateMapHandler
from DatabaseDriver.DownloadMapHandler import DownloadMapHandler
from DatabaseDriver.SearchTableHandler import SearchTableHandler
from DatabaseDriver.ShowInteractives import ShowInteractivesHandler

db_manager = Manager(database=database)
Maps.create_table()
Forks.create_table()
Interactives.create_table()


async def __create_fork_row(master_map_id, fork_id):
	await db_manager.create(Forks,
								master=master_map_id,
								fork=fork_id)


__create_map_handler = CreateMapHandler(db_manager, Maps, Interactives)
__download_map_handler = DownloadMapHandler(db_manager, Maps)
__search_map_handler = SearchTableHandler(db_manager, Maps, Forks)
__show_interactives_handler = ShowInteractivesHandler(db_manager, Maps, Interactives)
create_map = __create_map_handler.handle
download_map = __download_map_handler.handle
search_map = __search_map_handler.handle
fork_map = __create_fork_row
show_interactives = __show_interactives_handler.handle