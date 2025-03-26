import peewee
import json
from my_database.models import BaseModel


class Roles(BaseModel):
    """
    Represents the roles in the system
    Attributes:
        role_name (str): The name of the role.
        role_permissions (str): The permissions of the role.
        role_colour (str): The colour of the role.
        role_source (str): The source of the role.
        hoist (bool): Whether the role is hoisted.
        mentionable (bool): Whether the role is mentionable.
        min_points (int): The minimum points required to achieve the role.
        max_points (int): The maximum points required to keep the role.
    """
    role_name = peewee.CharField(max_length=100, unique=True)
    role_permissions = peewee.CharField(max_length=255)
    role_colour = peewee.CharField(max_length=255)
    role_source = peewee.CharField(max_length=255, default='DEFAULT')
    hoist = peewee.BooleanField()
    mentionable = peewee.BooleanField()
    min_points = peewee.IntegerField()
    max_points = peewee.IntegerField()

    @staticmethod
    def initalize_roles():
        """Loads the roles from roles.json and inserts them into the database"""
        filename = "roles.json"
        try:
            with open(filename, "r", encoding="utf-8") as json_file:
                roles_config = json.load(json_file)

            for _ , role_data in roles_config.items():
                if not Roles.get_or_none(Roles.role_name == role_data['role_name']):
                    print(f'New rule found in {filename}. Inserting {role_data["role_name"]} to the database')
                    Roles.add_roles(**role_data)

        except Exception as e:
            print(f'An error occured when importing Roles config from {json_file}')

    @staticmethod
    def add_roles(**kwargs):
        role = Roles.create(**kwargs)
        return role

