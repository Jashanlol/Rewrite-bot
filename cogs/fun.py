import discord
from discord.ext import commands
import os

from .utils import constants
from .utils.dataIO import dataIO

import random


class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.luckynumbers = dataIO.load_json("data/luckynumbers/luckynumbers.json")


    def save_settings(self):
        dataIO.save_json("data/luckynumbers/luckynumbers.json", self.luckynumbers)

    @commands.command()
    async def luckynumber(self, ctx):
        if str(ctx.guild.id) in self.luckynumbers:
            luckynumber = self.luckynumbers[str(ctx.guild.id)]
        else:
            luckynumber = "None"
        await ctx.send("Lucky Number for {} is {}".format(ctx.guild.name, luckynumber))

    @commands.command()
    async def setluckynumber(self, ctx, number: int):
        self.luckynumber[str(ctx.guild.id)] = number
        self.save_settings
        await ctx.send("Number saved")


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


def check_folders():
    if not os.path.exists("data/luckynumbers"):
        print("Creating data/luckynumbers folder...")
        os.makedirs("data/luckynumbers")


def check_files():
    if not os.path.exists("data/luckynumbers/luckynumbers.json"):
        print("Creating data/luckynumbers/luckynumbers.json file...")
        dataIO.save_json("data/luckynumbers/luckynumbers.json", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Fun(bot))

