import discord as dis
from discord.ext import commands


class Slapper(commands.Converter):
    use_nicknames : bool

    def __init__(self, *,use_nicknames) -> None:
        self.use_nicknames = use_nicknames

    async def convert(self, ctx, user : dis.Member):
        someone = user
        nickname = ctx.author
        #print(nickname)
        
        if self.use_nicknames:
            nickname = ctx.author.name
            
        return f"{nickname} slaps {someone}"