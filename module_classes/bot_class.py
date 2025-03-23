from discord.ext import commands
from module_classes.ranks import Ranks
import discord as dis


class DiscordBot(commands.Bot):
    ranks : Ranks

    def initialise(self):
        self.ranks = Ranks()

    async def process_message(self, message: dis.Message):
       await self.ranks.process_message(message)
    
    async def process_reaction(self, payload: dis.RawReactionActionEvent):
        member = await self.fetch_user(payload.user_id)
        await self.ranks.process_reaction(payload, member)
    
    async def process_thread(self, thread: dis.Thread):
        await self.ranks.process_thread(thread)