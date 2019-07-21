import random

import aiohttp
import discord
from discord.ext import commands

from .utils import constants


class Fun(commands.Cog):
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

    @commands.group(invoke_without_command=True)
    async def joke(self, ctx):
        return

    @joke.command()
    async def chuck(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://api.icndb.com/jokes/random?exclude=[explicit]') as r:
                res = await r.json()
                await ctx.send(res["value"]["joke"])

    @joke.command()
    async def yomama(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.apithis.net/yomama.php') as r:
                res = await r.text()
                await ctx.send(res)

    @commands.group(invoke_without_command=True)
    async def fact(self, ctx):
        return

    @fact.command()
    async def random(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://fact.birb.pw/api/v1/'+random.choice(['cat','dog'])) as r:
                res = await r.json()
                await ctx.send(res['string'])

    @fact.command()
    async def numbers(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://numbersapi.com/random/'+random.choice(['trivia','math','date','year'])) as r:
                res = await r.text()
                await ctx.send(res)

    @commands.group(name='def',invoke_without_command=True)
    async def _def(self, ctx, *, word):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.apithis.net/dictionary.php?define='+word) as r:
                res = await r.text()
                await ctx.send(res)

    @_def.command()
    async def example(self, ctx, *, word):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.apithis.net/dictionary.php?example='+word) as r:
                res = await r.text()
                await ctx.send(res)

    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://meme-api.explosivenight.us/v1/random/?type=json') as r:
                res = await r.json()
                e = discord.Embed(color=ctx.author.color)
                url = res["url"]
                e.set_image(url=url)
                await ctx.send(embed=e)
def setup(bot):
    bot.add_cog(Fun(bot))

