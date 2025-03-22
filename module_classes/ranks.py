import discord as dis
from user_activity.models import UserActivity, PointType
from users.model import User


class Ranks:
    async def process_message(self, message: dis.Message):
        print(f"Message {message.id} sent by {message.author}" )
        await self.add_points(message.id, message.author.id, PointType.MESSAGE)
    
    async def process_reaction(self, payload: dis.RawReactionActionEvent):
        if payload.event_type == 'REACTION_ADD':
            print(f"Reaction added by user {payload.user_id} on message {payload.message_id} with emoji {payload.emoji}")
            await self.add_points(payload.message_id, payload.user_id, PointType.REACTION)
        else:
            await self.reduce_points(payload.message_id, payload.user_id, PointType.REACTION, UserActivity.MODE_REDUCE)
    
    def _save_to_db(self, message_id: int, user_id: int, point_type: PointType, mode: str = UserActivity.MODE_ADD):
        user = User.fetch_user_by_id(user_id)
        user_activity = UserActivity(message_id=message_id, user=user)
        user_activity.record_new_points(point_type, mode)

    async def add_points(self, message_id, user_id, point_type):
        self._save_to_db(message_id, user_id, point_type)

    async def reduce_points(self, message_id, user_id, point_type, mode: str):
        self._save_to_db(message_id, user_id, point_type, mode)