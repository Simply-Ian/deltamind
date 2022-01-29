import peewee_asyncext
from peewee import Model, CharField, IntegerField, TextField, DateField, ForeignKeyField
from playhouse.postgres_ext import ArrayField
from playhouse.db_url import connect
import os


# postgres://tgkcvtovpaodej:b9d0ff843daca5dd9104661b6360bff34962287776f5b4221806f96d5f1afa12@ec2-54-78-36-245.eu-west-1.compute.amazonaws.com:5432/d6vmbi96rjrm3
db_url = os.environ.get('DATABASE_URL').split(':')
db_url[0] = 'postgresext'
db_url = ':'.join(db_url)
print(db_url)
database = connect(db_url)
# postgresql://postgres:my_password@localhost:5432/
# postgres://postgres:26082005@127.0.0.1:5432/delta
# database = peewee_asyncext.PostgresqlExtDatabase(database=db_url['database'],
# 						user=db_url['user'],
# 						password=db_url['password'],
# 						host=db_url['host'],
# 						port=db_url['port'])


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