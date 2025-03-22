#local files
#from custom_converter_class import Slapper
from cogs.module_classes.bot_class import DiscordBot
from users.model import User
from user_activity.models import UserActivity
#external libraries/modules
from discord.ext import commands
import discord as dis
import settings
import database


cogs = ['cogs.error_handler', 'cogs.greetings', 'cogs.cogs']


def setup_tables():
    database.db.create_tables([User, UserActivity])

def runtime():
    
    setup_tables()
    intents = dis.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True 
    intents.messages = True

    bot = DiscordBot(command_prefix='!', intents=intents)
    bot.initialise()


    @bot.event
    async def on_ready():
        for cog in cogs:
            await bot.load_extension(cog)
    
    @bot.command(
        help = 'Outputs information about bots connection latency.',
        description = 'Outputs information about bots'' connection latency',
        brief = 'Outputs Bot ping',
        enabled = True,
        hidden = False #invisible in !help
    )
    async def ping(ctx):
        await ctx.send('pong')

    @bot.command(
        help = 'Outputs date when a specified user joined the discord channel',
        description = 'Outputs date when a specified user joined the discord channel',
        brief = 'Outputs users'' join date',
        enabled = True,
        hidden = False
    )
    async def joined(ctx, user : dis.Member):
        user_joined = str(user)+': ' + str(user.joined_at)
        await ctx.send(user_joined)

    
    @bot.event
    async def on_message(message: dis.Message):
        ctx = await bot.get_context(message)
        await bot.process_commands(message)
        if not ctx.valid:
            if not message.author.bot:
                await bot.process_message(message)
            

    @bot.event
    async def on_raw_reaction_add(payload: dis.RawReactionActionEvent):
        await bot.process_reaction(payload)
    
    @bot.event
    async def on_raw_reaction_remove(payload: dis.RawReactionActionEvent):
        await bot.process_reaction(payload)
        
    bot.run(settings.DISCORD_API_SECRET, root_logger= True)


if __name__ == '__main__':
    
    runtime()