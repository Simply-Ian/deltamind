import peewee_asyncext
from peewee import Model, CharField, IntegerField, TextField, DateField, ForeignKeyField
from playhouse.postgres_ext import ArrayField


database = peewee_asyncext.PostgresqlExtDatabase(database='delta',
						user='postgres',
						password='26082005',
						host='localhost',
						port='5432')


class BaseModel(Model):

	class Meta:
		database = database


class Maps(BaseModel):
	title = CharField(80)
	author_nickname = CharField(80)
	creating_date = DateField()
	user_pass = CharField(20)
	admin_pass = CharField(20)
	map_code = ArrayField(TextField)


class Forks(BaseModel):
	master = ForeignKeyField(Maps)
	fork = ForeignKeyField(Maps)


class Interactives(BaseModel):
	interactive_type = CharField(2)
	master_map = ForeignKeyField(Maps)
	value = TextField()
	text_hint = TextField()
	combo_items = ArrayField(TextField)
	map_inner_ident = IntegerField()