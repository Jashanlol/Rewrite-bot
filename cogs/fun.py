import discord
from discord.ext import commands

from .utils import constants

import random


class Fun:
    def __init__(self, bot):
        self.bot = bot

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
    async def cool(self, ctx, *, member: discord.Member=None):
        if member is None:
            await ctx.send(ctx.author + random.choice(["'s cool :dark_sunglasses", "'s not cool :confused"]))
        elif member.name == 'Jashan':
            await ctx.send("Jashan's cool :dark_sunglasses:")
        elif member.bot is False:
            await ctx.send(member.name + "'s " + (random.choice(["cool :dark_sunglasses:", "not cool :confused:"])))
        else:
            await ctx.send("I'm cool :dark_sunglasses:")

    @commands.command(name="8ball")
    async def _ball(self, ctx):
        e = discord.Embed(description=ctx.author.mention + random.choice(constants.ball), color=ctx.author.color)
        await ctx.send(embed=e)

    @commands.command()
    async def hello(self, ctx):
        author = str(ctx.author)
        await ctx.send('Hello '+ author+ '!')


def setup(bot):
    bot.add_cog(Fun(bot))

