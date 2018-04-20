import discord
from discord.ext import commands
import os

from .utils import constants
from .utils.dataIO import dataIO

import random


class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.rolemanager = dataIO.load_json("data/rolemanager/rolemanager.json")


    def save_settings(self):
        dataIO.save_json("data/rolemanager/rolemanager.json", self.rolemanager)

    @commands.command()
    async def roles(self, ctx):
        if str(ctx.guild.id) in self.rolemanager:
            rolemanager = self.rolemanager[str(ctx.guild.id)]
        else:
            rolemanager = "None"
        await ctx.send("For {} bot can add roles: {}".format(ctx.guild.name, rolemanager))

    @commands.command()
    async def roleconfigadd(self, ctx, role: discord.Role):
        self.rolemanager[str(ctx.guild.id)] = role.id
        self.save_settings()
        await ctx.send("Role(s) saved")

    @commands.command()
    async def roleme(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=)
        await ctx.author.add_roles(role)

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
    if not os.path.exists("data/rolemanager"):
        print("Creating data/rolemanager folder...")
        os.makedirs("data/rolemanager")


def check_files():
    if not os.path.exists("data/rolemanager/rolemanager.json"):
        print("Creating data/rolemanager/rolemanager.json file...")
        dataIO.save_json("data/rolemanager/rolemanager.json", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Fun(bot))

