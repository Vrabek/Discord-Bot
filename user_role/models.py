from peewee import Model, CharField, IntegerField
from database import db

class UserRole(Model):
    """
    Represents a user's role in the system.
    Attributes:
        user_id (str): A unique identifier for the user.
        user_nickname (str): The nickname of the user.
        total_points (int): The total points accumulated by the user.
        role_name (str): The name of the role.
    """
    user_id = CharField(100)
    user_nickname = CharField(256)
    total_points = IntegerField()
    role_name = CharField(100)

    class Meta:
        database = db
        table_name = 'USER_ROLE'  # Name of the view in the database
        primary_key = False