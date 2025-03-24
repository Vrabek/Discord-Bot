import discord as dis
from discord.ext import commands
from module_classes.ranks import Ranks
from module_classes.roles import RoleMenager


class DiscordBot(commands.Bot):
    ranks : Ranks
    role_menager : RoleMenager

    def initialise(self):
        self.ranks = Ranks()
        self.role_menager = RoleMenager()

    async def initialize_roles(self):
        await self.role_menager.initalize_roles()
        
    async def process_message(self, message: dis.Message):
       await self.ranks.process_message(message)
    
    async def process_reaction(self, payload: dis.RawReactionActionEvent):
        member = await self.fetch_user(payload.user_id)
        await self.ranks.process_reaction(payload, member)
    
    async def process_thread(self, thread: dis.Thread):
        await self.ranks.process_thread(thread)