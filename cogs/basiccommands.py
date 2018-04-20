import discord
from discord.ext import commands

from .utils import constants

import os
import datetime
import random


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
    async def avatar(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        e = discord.Embed()
        e.set_image(url=member.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def date(self, ctx):
        await ctx.send(datetime.date.today())

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
    async def info(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        roles = [role.name.replace('@', '@\u200b') for role in member.roles]
        shared = sum(1 for m in self.bot.get_all_members() if m.id == member.id)
        e = discord.Embed()
        e.set_author(name=member, icon_url=member.avatar_url)
        e.add_field(name='ID', value=member.id)
        e.add_field(name='Servers', value=f'{shared} shared')
        e.add_field(name='Created', value=member.created_at)
        e.add_field(name='Nickname', value=member.nick)
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles')
        e.color = member.color
        e.set_footer(text='Member Since').timestamp = member.joined_at
        e.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def roleme(self, ctx, *, role: discord.Role):
        await ctx.author.add_roles(role)

    @commands.command()
    async def hello(self, ctx):
        author = str(ctx.author)
        await ctx.send('Hello '+ author+ '!')

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send('Shutting down...')
        await bot.logout()

    @commands.command()
    async def uptime(self, ctx):
        # Get's process id and returns uptime in seconds
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

    @commands.command()
    async def create_emoji(self, ctx, *, name:str):
        await ctx.message.attachments[0].save("temp.jpg")
        with open('temp.jpg', 'rb') as fp:
                await ctx.guild.create_custom_emoji(name=name, image=fp.read())
        os.remove("temp.jpg")

def setup(bot):
    bot.add_cog(BasicCommands(bot))

