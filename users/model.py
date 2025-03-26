import peewee
from my_database.models import BaseModel

class User(BaseModel):
    """
    Represents a user in the system.
    Attributes:
        user_id (str): A unique identifier for the user.
        user_nickname (str): The nickname of the user.
        total_points (float): The total points accumulated by the user. Defaults to 0.
    """
    user_id = peewee. CharField(max_length=100)
    user_nickname = peewee.CharField(max_length=256)
    total_points = peewee.FloatField(default=0)

    @staticmethod
    def fetch_user_by_id(user_id: str,user_nickname: str = None):
        try:
            user = User.get(User.user_id == user_id)
        except:
            user = User.create(user_id=user_id, user_nickname = user_nickname)
        return user
    
    @staticmethod
    def get_leaderboard(limit=10) -> peewee.ModelSelect:
        return User.select().order_by(User.total_points.desc()).limit(limit)