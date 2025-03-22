from discord.ext import commands
from cogs.module_classes.ranks import Ranks
import discord as dis


class DiscordBot(commands.Bot):
    ranks : Ranks

    def initialise(self):
        self.ranks = Ranks()

    async def process_message(self, message: dis.Message):
       await self.ranks.process_message(message)
    
    async def process_reaction(self, payload: dis.RawReactionActionEvent):
        await self.ranks.process_reaction(payload)
    