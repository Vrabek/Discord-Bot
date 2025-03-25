#local files
from module_classes.bot_class import DiscordBot
from users.model import User
from user_activity.models import UserActivity
from roles.models import Roles
#external libraries/modules
from discord.ext import commands
import discord as dis
import settings
import database
import json


cogs = ['cogs.error_handler', 'cogs.greetings', 'cogs.cogs']


def setup_db_objects():
    #creates all the tables in the database
    database.db.create_tables([User, UserActivity, Roles])
    #creates views from sql_views.json
    database.init_views()
    #populates the Roles table with default roles from roles.json
    Roles.initalize_roles()
    print('Database objects created!')

def runtime():
    
    setup_db_objects()
    
    """TODO Need to dump it elsewhere"""
    try:
        with open("intents.json", "r") as json_file:
            intents_config = json.load(json_file)

        intents = dis.Intents.default()

        for key, value in intents_config.items():

            if hasattr(intents, key):
                setattr(intents, key, value == "True")
    except:
        print(f'An error occured when importing Intents config from {json_file}')

    bot = DiscordBot(command_prefix='!', intents=intents)
    bot.initialise()
     


    @bot.event
    async def on_ready():
        for cog in cogs:
            await bot.load_extension(cog)
        
        # create roles inside the guild from the database
        await bot.initialize_db_roles()
        # hopefully manages the roles based on the user_role view
        await bot.apply_roles_from_user_role_view()
        print('Bot is ready!')
    
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
        if not payload.member.bot:
            await bot.process_reaction(payload)
    
    @bot.event
    async def on_raw_reaction_remove(payload: dis.RawReactionActionEvent):
        if not payload.member.bot:
            await bot.process_reaction(payload)

    @bot.event
    async def on_socket_event_type(data):
        # My little helper
        print(f'Socket response received! {data}')
    
    @bot.event
    async def on_thread_create(thread):
        if not thread.author.bot:
            await bot.process_thread(thread)
        
    bot.run(settings.DISCORD_API_SECRET, root_logger= True)


if __name__ == '__main__':
    
    runtime()