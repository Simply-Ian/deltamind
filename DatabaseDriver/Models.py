import peewee_asyncext
from peewee import Model, CharField, IntegerField, TextField, DateField, ForeignKeyField
from playhouse.postgres_ext import ArrayField
from playhouse.db_url import parse
import os


db_url = parse(os.environ.get('DATABASE_URL'))
print(db_url)
# postgresql://postgres:my_password@localhost:5432/
# postgres://postgres:26082005@127.0.0.1:5432/delta
database = peewee_asyncext.PostgresqlExtDatabase(database=db_url['database'],
						user=db_url['user'],
						password=db_url['password'],
						host=db_url['host'],
						port=db_url['port'])


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