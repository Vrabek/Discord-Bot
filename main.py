from discord.ext import commands
import discord as dis
import settings

def test():

    api_str = settings.DISCORD_API_SECRET
    intents = dis.Intents.default()

    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.run(settings.DISCORD_API_SECRET)

    print(api_str)


if __name__ == '__main__':
    
    test()