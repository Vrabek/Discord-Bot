#local files
#from custom_converter_class import Slapper
from cogs.module_classes.bot_class import DiscordBot
from users.model import User
from models import UserActivity
#external libraries/modules
from discord.ext import commands
import discord as dis
import settings
import database




cogs = ['cogs.error_handler', 'cogs.greetings']


def setup_tables():
    database.db.create_tables([User, UserActivity])

def runtime():
    
    
        #logger.info(f"Settting up tables" )
    setup_tables()
        #logger.info(f"Table setup has finished succesfully" )
    
        #logger.info(f"Table setup has failed" )

    
    intents = dis.Intents.default()
    intents.message_content = True

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
        help = 'Outputs string supplied by user.',
        description = 'Outputs string supplied by user.',
        brief = 'Outputs user string',
        enabled = True,
        hidden = False
    )
    async def say(ctx, *params):
        if not params:
            await ctx.send('No data was supplied')
        else:
            await ctx.send(" ".join(params))

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
        print(ctx)
        if not ctx.valid:
            if not message.author.bot:
                await bot.process_message(message)
        #await bot.process_message(message)

    @bot.event
    async def on_raw_reaction_add(payload: dis.RawReactionActionEvent):
        await bot.process_reaction(payload)
    
    @bot.event
    async def on_raw_reaction_remove(payload: dis.RawReactionActionEvent):
        await bot.process_reaction(payload)
        
    bot.run(settings.DISCORD_API_SECRET, root_logger= True)


if __name__ == '__main__':
    
    runtime()