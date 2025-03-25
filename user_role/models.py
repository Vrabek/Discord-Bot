from peewee import Model, CharField, IntegerField
from database import db

class UserRole(Model):
    user_id = CharField(100)
    user_nickname = CharField(256)
    total_points = IntegerField()
    role_name = CharField(100)

    class Meta:
        database = db
        table_name = 'USER_ROLE'  # Name of the view in the database
        primary_key = False