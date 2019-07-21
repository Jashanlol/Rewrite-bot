import datetime
import traceback

from discord.ext import commands

from safety import token

initial_cogs = ["cogs.admin", "cogs.fun", "cogs.utilities", "cogs.roles", "cogs.tags", "cogs.stars","cogs.points"]

bot = commands.Bot(command_prefix='r.')

@bot.event
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    bot.uptime = datetime.datetime.utcnow()

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
    except Exception as exc:
        traceback_text = "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__, 4))
        print(traceback_text)

bot.run(token)