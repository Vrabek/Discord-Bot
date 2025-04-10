import discord as dis
from discord.ext import commands
from module_classes.ranks import Ranks
from module_classes.roles import RoleMenager


class DiscordBot(commands.Bot):
    ranks : Ranks
    role_menager : RoleMenager
    #mój serwer
    #GUILD_ID = 1333466935815442462
    #rokitnik = 188675437092798465
    GUILD_ID = 188675437092798465

    def initialise(self):
        self.ranks = Ranks()
        self.role_menager = RoleMenager()

    """Ranks methods"""
    async def process_message(self, message: dis.Message):
       await self.ranks.process_message(message)
    
    async def process_reaction(self, payload: dis.RawReactionActionEvent):
        member = await self.fetch_user(payload.user_id)
        await self.ranks.process_reaction(payload, member)
    
    async def process_thread(self, thread: dis.Thread):
        await self.ranks.process_thread(thread)
        
    """Roles methods"""
    async def initialize_db_roles(self, GUILD_ID=GUILD_ID):
        guild_id = GUILD_ID
        guild = self.get_guild(guild_id)
        await self.role_menager.initialiaze_db_roles(guild)

    async def apply_roles_from_user_role_view(self, GUILD_ID=GUILD_ID):
        guild_id = GUILD_ID
        guild = self.get_guild(guild_id)
        await self.role_menager.apply_roles_from_user_role_view(guild)