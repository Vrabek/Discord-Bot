import peewee
import json
from my_database.models import BaseModel


class Roles(BaseModel):
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
        filename = "roles.json"
        try:
            with open(filename, "r", encoding="utf-8") as json_file:
                roles_config = json.load(json_file)

            for _ , role_data in roles_config.items():
                #print(f' Data checked {role_data['role_name']}')
                if not Roles.get_or_none(Roles.role_name == role_data['role_name']):
                    print(f'New rule found in {filename}. Inserting {role_data["role_name"]} to the database')
                    Roles.add_roles(**role_data)

        except Exception as e:
            print(f'An error occured when importing Roles config from {json_file}')

    @staticmethod
    def add_roles(**kwargs):
        role = Roles.create(**kwargs)
        return role

