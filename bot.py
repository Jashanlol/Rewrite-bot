import discord
from discord.ext import commands
from safety import token
import traceback
import datetime

initial_cogs = ["cogs.admin", "cogs.fun", "cogs.utilities", "cogs.roles", "cogs.tags", "cogs.stars"]

bot = commands.Bot(command_prefix='r.')

@bot.event
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author != bot.user:
        if message.content.startswith('no u'):
            await message.channel.send("**"+message.content+"**")
        if message.content.startswith('***no u'):
            await message.channel.send(message.content)
        if message.content.startswith('*no u'):
            await message.channel.send(message.content)
    else:
        pass


for cog in initial_cogs:
    try:
        bot.load_extension(cog)
    except Exception as exc:
        traceback_text = "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__, 4))
        print(traceback_text)

bot.run(token)