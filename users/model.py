import peewee
from cogs.module_classes.models import BaseModel

class User(BaseModel):
    user_id = peewee. CharField(max_length=100)
    total_points = peewee.FloatField(default=0)

    @staticmethod
    def fetch_user_by_id(user_id):
        try:
            user = User.get(User.user_id == user_id)
        except:
            user = User.create(user_id=user_id)
        return user