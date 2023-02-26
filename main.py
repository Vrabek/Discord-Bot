#local files
from custom_converter_class import Slapper

#external libraries/modules
from discord.ext import commands
import discord as dis
import settings

logger = settings.logging.getLogger('bot')
cogs = ['cogs.error_handler', 'cogs.greetings']

def runtime():

    intents = dis.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)


    @bot.event
    async def on_ready():
        logger.info(f"Bot: {bot.user} ID: {bot.user.id} is ready!" )
        for cog in cogs:
            logger.info(f"Loading: {cog} in progress" )
            await bot.load_extension(cog)
            logger.info(f"Loading: {cog} has finished" )

    
    @bot.command(
        help = 'Outputs information about bots connection latency.',
        description = 'Outputs information about bots'' connection latency',
        brief = 'Outputs Bot ping',
        enabled = True,
        hidden = False #invisable in !help
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
        user_joined = str(user)+': '+str(user.joined_at)
        await ctx.send(user_joined)


    @bot.command(
        help = 'Slaps specified user',
        description = 'Slaps specified user',
        brief = 'slap the fucker',
        enabled = True,
        hidden = False
    )
    async def bitchslap(ctx, user : Slapper(use_nicknames=True)):      
        await ctx.send(user)

    bot.run(settings.DISCORD_API_SECRET, root_logger= True)


if __name__ == '__main__':
    
    runtime()