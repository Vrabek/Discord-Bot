import discord
from discord.ext import commands 

class Greetings(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'nigga' in message.content:
            await message.add_reaction("✅")
    
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member):
        await ctx.send(f"Hello {member.name}")
        
async def setup(bot):
    await bot.add_cog(Greetings(bot))