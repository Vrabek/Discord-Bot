import enum
import peewee
from users.model import User
from my_database.models import BaseModel

class PointType(enum.Enum):
    # Activity Types and their corresponding points
    MESSAGE = 3
    COMMAND = 2
    REACTION = 1
    THREAD = 5

    @property
    def point_name(self):
        return self.name

class PointSubType(enum.Enum):
    # Activity Subtypes and their corresponding points
    MENTION_ALL = 1
    MENTION_ROLE = 2
    MENTION_USER = 3
    MENTION_CHANNEL = 4
    ATTACHMENT = 5
    STICKER = 6
    TTS = 7
    UNSPECIFIED = 0

    @property
    def point_name(self):
        return self.name
    
class UserActivity(BaseModel):
    MODE_ADD = 'ADD'
    MODE_REDUCE = 'REDUCE'

    MODE_CHOICES = (
        (MODE_ADD, MODE_ADD),
        (MODE_REDUCE, MODE_REDUCE)
    )

    user = peewee.ForeignKeyField(model=User)
    activity_id = peewee.CharField(max_length=255)
    activity_type = peewee.CharField(max_length=255, default='MESSAGE')
    activity_subtype = peewee.CharField(max_length=255, null=True)
    points = peewee.FloatField()
    mode = peewee.CharField(choices= MODE_CHOICES, default=MODE_ADD)

    def record_new_points(self, point_type: PointType, point_subtype: PointSubType, mode: str):

        points = point_type.value + point_subtype.value
        current_total_points = UserActivity.get_points(self.user.user_id)

        if mode == UserActivity.MODE_ADD:
            new_total_points = current_total_points + points
        else:
            new_total_points = current_total_points - points

        self.user.total_points = new_total_points
        self.activity_type = point_type.point_name
        self.activity_subtype = point_subtype.point_name
        self.points = points
        self.mode = mode
        self.user.save()
        self.save()
    
    @staticmethod
    def get_points(user_id):
        added_points_sum = UserActivity.select(
            UserActivity.points, peewee.fn.SUM(UserActivity.points).alias("total")
        ).join(User).where(User.user_id == user_id, UserActivity.mode == UserActivity.MODE_ADD)

        reduced_points_sum = UserActivity.select(
            UserActivity.points, peewee.fn.SUM(UserActivity.points).alias("total")
        ).join(User).where(User.user_id == user_id, UserActivity.mode == UserActivity.MODE_REDUCE)

        added_total = 0
        if added_points_sum[0].total:
            added_total = added_points_sum[0].total

        reduced_total = 0
        if reduced_points_sum[0].total:
            reduced_total = reduced_points_sum[0].total

        return added_total - reduced_total

