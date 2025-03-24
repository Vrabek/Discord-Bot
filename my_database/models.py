import peewee
import datetime
import database
import json

class BaseModel(peewee.Model):
    created_dt = peewee.DateTimeField(default = datetime.datetime.now)
    moodified_dt = peewee.DateTimeField()

    def save(self, *args, **kwargs):
        self.moodified_dt = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
    

    class Meta:
        database = database.db

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

        if Roles.select().count() == 0:
            try:
                with open("roles.json", "r", encoding="utf-8") as json_file:
                    roles_config = json.load(json_file)

                for role_id, role_data in roles_config.items():
                    Roles.add_roles(**role_data)
            except:
                print(f'An error occured when importing Roles config from {json_file}')

    @staticmethod
    def add_roles(**kwargs):
        role = Roles.create(**kwargs)
        return role

