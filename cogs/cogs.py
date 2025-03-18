import discord
import discord.ext.commands as commands
from users.model import User

class Ranks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ranksys(self, ctx):
            '''Rank system commands group'''
            if ctx.invoked_subcommand is None:
                 await ctx.send('Invalid ranksys command.')

    @ranksys.command()
    async def leaderboard(self, ctx, limit: int = 10):
            """Shows the top users ranked by points
    
            Args:
                limit (int, optional): Number of users to show (max 10). Defaults to 10.
            """
            print("Leaderboard command")
            if limit > 10:
                limit = 10
            leaderboard = User.get_leaderboard(limit)
            embed = discord.Embed(title="Leaderboard", description="Top 10 users", color=0x00ff00)
            for user in leaderboard:
                embed.add_field(name=user.user_id, value=user.total_points, inline=False)

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Ranks(bot))