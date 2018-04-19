import discord
from discord.ext import commands
from safety import token
import random
import datetime
from constants import *
import math

bot = commands.Bot(command_prefix='r.')

@bot.event
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')

class BasicCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Ping...Pong')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(decription='Echo...Echo...Echo')
    async def echo(self, ctx, *, msg:str = None):
        if msg is None:
            await ctx.send('I need something to echo!')
        else:
            await ctx.send(msg)

    @commands.command(description='When you wanna settle the score')
    async def choice(self, ctx, *choice:str):
        await ctx.send(random.choice(choice))

    @commands.command(description='<# of dice> + d + <# of sides> <----(one word)')
    async def roll(self, ctx, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='Flip a coin, any coin!')
    async def flip(self, ctx):
        await ctx.send(random.choice(['Heads!', 'Tails!']))

    @commands.command()
    async def edit(self, ctx, *, name:str=None):
        if name is None:
            await ctx.send('I need something to change your name to!')
        await ctx.author.edit(nick=name)

    @commands.command()
    async def avatar(self, ctx, *,member: discord.Member=None):
        if member is None:
            await ctx.send(ctx.author.avatar_url_as(format=None))
        await ctx.send(member.avatar_url_as(format=None))

    @commands.command()
    async def date(self, ctx):
        await ctx.send(datetime.date.today())

    @commands.command()
    async def cool(self, ctx, *, member: discord.Member=None):
        if member is None:
            await ctx.send('You need to tag a member for me.')
        elif member.name == 'Jashan':
            await ctx.send("Jashan's cool :dark_sunglasses:")
        elif member.bot is False:
            await ctx.send(member.name + "'s " + (random.choice(["cool :dark_sunglasses:", "not cool :confused:"])))
        else:
            await ctx.send("I'm cool :dark_sunglasses:")

    @commands.command(name="8ball")
    async def _ball(self, ctx):
        e = discord.Embed(description=ctx.author.mention + random.choice(ball), color=ctx.author.color)
        await ctx.send(embed=e)


bot.add_cog(BasicCommands(bot))
bot.run(token)