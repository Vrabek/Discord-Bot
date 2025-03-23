import discord as dis
from user_activity.models import UserActivity, PointType, PointSubType
from users.model import User


class Ranks:
    async def process_message(self, message: dis.Message):
        print(f"Message {message.id} sent by {message.author}")
        point_type = self.__determine_point_type(message)
        await self.add_points(message.id, message.author.id, message.author, PointType.MESSAGE, point_type)

    async def process_reaction(self, payload: dis.RawReactionActionEvent, member: dis.User):

        if payload.event_type == 'REACTION_ADD':
            print(f"Reaction added by user {member.name} on message {payload.message_id} with emoji {payload.emoji}")
            await self.add_points(payload.message_id, payload.user_id, member.name, PointType.REACTION)
        else:
            await self.reduce_points(payload.message_id, payload.user_id, member.name, PointType.REACTION, mode=UserActivity.MODE_REDUCE)

    async def process_thread(self, thread: dis.Thread):
        print(f"Thread {thread.id} created by {thread.owner}")
        await self.add_points(thread.id, thread.owner_id, thread.owner, PointType.THREAD)
    

    async def add_points(self, 
                         message_id, 
                         user_id, 
                         user_nickname, 
                         point_type,
                         point_subtype = PointSubType.UNSPECIFIED):
        
        self._save_to_db(message_id, user_id, user_nickname, point_type, point_subtype)

    async def reduce_points(self, 
                            message_id, 
                            user_id, 
                            user_nickname, 
                            point_type,
                            point_subtype = PointSubType.UNSPECIFIED,
                            mode: str = UserActivity.MODE_REDUCE):
        
        self._save_to_db(message_id, user_id, user_nickname, point_type, point_subtype, mode)

    def _save_to_db(self, 
                    message_id: int,
                    user_id: int,
                    user_nickname: str,
                    point_type: PointType,
                    point_subtype: PointSubType,
                    mode: str = UserActivity.MODE_ADD):
        
        user = User.fetch_user_by_id(user_id, user_nickname)
        user_activity = UserActivity(activity_id=message_id, user=user)
        user_activity.record_new_points(point_type, point_subtype, mode)

    def __determine_point_type(self, message: dis.Message) -> PointSubType:
        ''''Yea.... even COPILOT couldn't handle this one'''
        if message.mention_everyone:
            return PointSubType.MENTION_ALL

        if len(message.mentions) > 0:
            return PointSubType.MENTION_USER

        if len(message.role_mentions) > 0:
            return PointSubType.MENTION_ROLE

        if len(message.channel_mentions) > 0:
            return PointSubType.MENTION_CHANNEL

        if len(message.attachments) > 0:
            return PointSubType.ATTACHMENT

        if len(message.stickers) > 0:
            return PointSubType.STICKER

        if message.tts:
            return PointSubType.TTS
        
        return PointSubType.UNSPECIFIED