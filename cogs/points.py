import discord
import asyncio
from random import randint
import discord.ext.commands as commands
from users.model import User
from user_activity.models import UserActivity
from module_classes.ranks import Ranks


class FakePointType:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    @property
    def point_name(self):
        return self.name

class Points(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def points(self, ctx):
            '''Points system commands subgroup'''
            if ctx.invoked_subcommand is None:
                 await ctx.send('Invalid ranksys command.')

    @points.command()
    async def leaderboard(self, ctx, limit: int = 10):
            """Shows top users ranked by points
    
            Args:
                limit (int, optional): Number of users to show (max 10). Defaults to 10.
            """
            print("Leaderboard command")
            if limit > 10:
                limit = 10
            leaderboard = User.get_leaderboard(limit)
            embed = discord.Embed(title="Leaderboard", description="Top 10 users", color=0x00ff00)
            for user in leaderboard:
                embed.add_field(name=user.user_nickname, value=user.total_points, inline=False)

            await ctx.send(embed=embed)

    @points.command(hidden = False)
    async def show(self, ctx):
        """Shows current users points"""

        response_dict = {1: 'I think',
                         2: 'But I am not sure',
                         3: 'Could be wrong though',
                         4: 'Without a doubt I am certain',
                         5: 'I guess',
                         6: 'Hmmm...',
                         7: ''}
        
        last_message = response_dict.get(randint(1,7))

        author = ctx.author
        current_sender_points = UserActivity.get_points(author.id)
        await ctx.send(f"Your current score is {current_sender_points} points")
        await asyncio.sleep(1)
        await ctx.send(last_message)


    @points.command()
    async def gift(self, ctx, user: discord.Member = None, points: int = 5):
            """Gifts points to a specified user (!points gift @user 10)

            Args:
                user (discord.Member): The user to give points to.
                points (float): The number of points to give.
            """
            sender = ctx.author
            current_sender_points = UserActivity.get_points(sender.id)
            if await self.__check_member_validity(ctx, sender, user) and \
               await self.__check_points_validity(ctx, current_sender_points, points):

                user_id = str(user.id)
                user_nickname = str(user.display_name)
                author_id = str(sender.id)
                author_nickname = str(sender.display_name)
                message_id = str(ctx.message.id)
                gift_point_type = FakePointType(name="GIFT", value=points)
                ranks = Ranks()
                await ranks.add_points(message_id, user_id, user_nickname, gift_point_type)
                await ranks.reduce_points(message_id, author_id, author_nickname, gift_point_type)


                await ctx.send(f"Given {points} points to {user.display_name}.")

        
    async def __check_points_validity(self, ctx, sender_total_points: int, points: int) -> bool:
        """Checks if the points are valid (greater than 0)"""
        if not isinstance(points, int):
            await ctx.send("Points must be a integer! \nLike 1, 3, 10... Dummy...")  
            return False     
        if points < 0:
            await ctx.send("What are you trying to do? \nPoints cannot be negative!")
            return False
        if sender_total_points < points:
            await ctx.send("You don't have enough points!")
            return False
        
        return True
    
    async def __check_member_validity(self, ctx, sender: discord.Member, recipient) -> bool:
        """Checks if the member is valid"""
        if recipient is None:
            await ctx.send("You must specify a member!")
        if not isinstance(recipient, discord.Member):
            await ctx.send("Member must be a valid Discord member!")
            return False
        #check if is not trying to give points to bot
        if recipient.bot:
            await ctx.send("Why... Just Why?")
            return False

        if recipient == sender:
            await ctx.send("You can't give points to yourself!")
            #wait 5 secend and then send another message
            await asyncio.sleep(3)
            #await ctx.send("You know what? I'll just take them away!")
            #await asyncio.sleep(1)
            await ctx.send("Eat my cyber-ass!")
            return False
        
        return True

async def setup(bot):
    await bot.add_cog(Points(bot))