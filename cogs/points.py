import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

import os
import random
import time
from .utils.dataIO import dataIO

class Points:

    def __init__(self, bot):
        self.bot = bot
        self.pointmanager = dataIO.load_json("data/pointmanager/pointmanager.json")

    def save_settings(self):
        dataIO.save_json("data/pointmanager/pointmanager.json", self.pointmanager)

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

    
    @commands.command()
    @commnads.guild_only()
    async def top(self, ctx):
        points_list = []
        for person_id, points_dict in self.pointmanager.items():
            points_list.append([person_id, points_dict["points"]])
        sorted_points_list = sorted(points_list, key=lambda x: x[1], reverse=True)
        string = ""
        for x in range(0,5):
            author = self.bot.get_user(int(sorted_points_list[x][0]))
            points = sorted_points_list[x][1]
            string += author.name + " " + str(points) + "\n"

        await ctx.send(string)




    @commands.command(invoke_without_command=True)
    @commands.guild_only()
    async def stats(self, ctx, *, member: discord.Member=None):
        if member is None:
            e = discord.Embed(color=ctx.author.color)
            member = ctx.author
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
            e.add_field(name="Points", value=self.pointmanager[str(ctx.author.id)]["points"])
            await ctx.send(embed=e)
        elif member is not None:
            if str(member.id) in self.pointmanager:
                e = discord.Embed(color=member.color)
                e.set_author(name=member.name, icon_url=member.avatar_url_as(format=None))
                e.add_field(name="Points", value=self.pointmanager[str(member.id)]["points"])
                await ctx.send(embed=e)

    @stats.error
    async def stats_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    async def poker(self, ctx, amount:int, *, member:discord.Member):
        if str(ctx.author.id) not in self.pointmanager:
            await ctx.send('{}, you need an account to play poker. Make one now with `r.register`.'.format(ctx.author.mention))
        elif str(member.id) not in self.pointmanager:
            await ctx.send('Member needs an account to play poker. {} make one now using `r.register`.'.format(member.mention))
        elif member is ctx.author:
            await ctx.send("Can't challenge yourself!")
        elif amount > self.pointmanager[str(ctx.author.id)]["points"]:
            await ctx.send('You do not have enough points to use that amount.')
        elif amount > self.pointmanager[str(member.id)]["points"]:
            await ctx.send('Challenged member only has {} points.'.format(self.pointmanager[str(member.id)]["points"]))
        else:
            await ctx.send("{} you have been challenged by {} in a game of poker! Do you accept or decline?"
                           "".format(member.mention, ctx.author.mention))
            def check(m):
                return m.channel == ctx.channel and m.author == member
            msg = await self.bot.wait_for('message', check=check)
            if msg.content == "accept":
                await ctx.send('Challenged accepted!')
                choice = random.choice(["author","member"])
                if choice == "author":
                    self.pointmanager[str(ctx.author.id)]["points"]+=amount
                    self.pointmanager[str(member.id)]["points"]-=amount
                    self.save_settings()
                    e = discord.Embed(title='Poker Outcome',color=ctx.author.color)
                    e.set_thumbnail(url=ctx.author.avatar_url_as(format=None))
                    e.add_field(name='Winner',value=ctx.author.name,inline=False)
                    e.add_field(name='Gained', value='{} gained {} points.'.format(ctx.author.name, amount, inline=False))
                    e.add_field(name='Lost', value= '{} lost {} points.'.format(member.name, amount),inline=False)
                    points = self.pointmanager[str(ctx.author.id)]["points"]
                    points2 = self.pointmanager[str(member.id)]["points"]
                    e.add_field(name='Overview', value='{} now has {} points.\n{} now has {} points.'.format(ctx.author.name,
                                                            points, member.name, points2),inline=False)
                    await ctx.send(embed=e)
                if choice == "member":
                    self.pointmanager[str(member.id)]["points"]+=amount
                    self.pointmanager[str(ctx.author.id)]["points"]-=amount
                    self.save_settings()
                    e = discord.Embed(title='Poker Outcome',color=member.color)
                    e.set_thumbnail(url=member.avatar_url_as(format=None))
                    e.add_field(name='Winner',value=member.name,inline=False)
                    e.add_field(name='Gained', value='{} gained {} points.'.format(member.name, amount),inline=False)
                    e.add_field(name='Lost', value= '{} lost {} points.'.format(ctx.author.name, amount),inline=False)
                    points = self.pointmanager[str(ctx.author.id)]["points"]
                    points2 = self.pointmanager[str(member.id)]["points"]
                    e.add_field(name='Overview', value='{} now has {} points.\n{} now has {} points.'.format(member.name,
                                                            points2, ctx.author.name, points),inline=False)
                    await ctx.send(embed=e)
            elif msg.content == 'decline':
                await ctx.send('Challenge declined! :frowning2:')

    @poker.error
    async def poker_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    async def register(self, ctx):
        if str(ctx.author.id) in self.pointmanager:
            await ctx.send('Your account is already registered.')
        else:
            self.pointmanager[str(ctx.author.id)] = {"points":0}
            self.save_settings()
            e=discord.Embed(color=ctx.author.color)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
            e.add_field(name="Points", value=self.pointmanager[str(ctx.author.id)]["points"])
            await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(rate=1,per=1.5,type=BucketType.user)
    async def slot(self, ctx):
        if str(ctx.author.id) not in self.pointmanager:
            await ctx.send('{}, you need an account to use the slot machine. Make one now with `r.register`.'.format(ctx.author.mention))
            return
        list = [":lemon:",":apple:",":pineapple:",":banana:",":grapes:"]
        choice1 = random.choice(list)
        choice2 = random.choice(list)
        choice3 = random.choice(list)
        if choice1 == choice2 == choice3:
            e=discord.Embed(color=ctx.author.color)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
            e.add_field(name='Slot Machine Results:',value="{} {} {}".format(choice1, choice2, choice3),inline=False)
            self.pointmanager[str(ctx.author.id)]["points"]+=100
            self.save_settings()
            points = self.pointmanager[str(ctx.author.id)]["points"]
            e.add_field(name="Overview:",value=':balloon: {}, you won 100 points!\nYou now have {} points'
                                               '!:balloon: '.format(ctx.author.mention, points))
            await ctx.send(embed=e)
        else:
            e=discord.Embed(color=ctx.author.color)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
            e.add_field(name='Slot Machine Results:',value="{} {} {}".format(choice1, choice2, choice3),inline=False)
            self.pointmanager[str(ctx.author.id)]["points"]-=2
            if self.pointmanager[str(ctx.author.id)]["points"] < 0:
                self.pointmanager[str(ctx.author.id)]["points"] = 0
            self.save_settings()
            points = self.pointmanager[str(ctx.author.id)]["points"]
            e.add_field(name="Overview:",value='{} , you lost 2 points.\nYou now have {} points!'.format(ctx.author.mention,
                                                                                                         points))
            await ctx.send(embed=e)

    @slot.error
    async def on_slot_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(rate=1,per=10,type=BucketType.user)
    async def bet(self, ctx, x:int):
        if str(ctx.author.id) not in self.pointmanager:
            await ctx.send('{}, you need an account to gamble. Make one now with `r.register`.'.format(ctx.author.mention))
            return
        choice = random.choice(["won","lost"])
        if str(ctx.author.id) not in self.pointmanager:
            await ctx.send('You have no points.')
        elif x <= self.pointmanager[str(ctx.author.id)]["points"]:
            if choice == "won":
                self.pointmanager[str(ctx.author.id)]["points"]+=x
            elif choice == "lost":
                self.pointmanager[str(ctx.author.id)]["points"]-=x
            points = self.pointmanager[str(ctx.author.id)]["points"]
            self.save_settings()
            e = discord.Embed(color=ctx.author.color)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
            e.add_field(name='Result',value="{} you {} {} points.".format(ctx.author.mention, choice,x),inline=False)
            e.add_field(name="Overview", value="You now have {} points.".format(self.pointmanager[str(ctx.author.id)]["points"],inline=False))
            await ctx.send(embed=e)
        else:
            await ctx.send('You do not have enough points to bet this amount.')
            return

    @bet.error
    async def bet_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

    async def on_member_join(self, member):
        if str(member.id) in self.pointmanager:
            self.pointmanager[str(member.id)]["points"]+=5
        else:
            self.pointmanager[str(member.id)] = {"points":5}
        self.save_settings()

    async def on_member_remove(self, member):
        if str(member.id) in self.pointmanager:
            self.pointmanager[str(member.id)]["points"]-=5
        else:
            await member.send('No points!')
        self.save_settings()

    @commands.command()
    @commands.guild_only()
    async def donate(self, ctx, amount:int, member: discord.Member):
        if member is ctx.author:
            await ctx.send('Cannot donate to yourself.')
        elif str(ctx.author.id) not in self.pointmanager:
            await ctx.send('{}, you need an account to donate. Make one now with `r.register`.'.format(ctx.author.mention))
        elif str(member.id) not in self.pointmanager:
            await ctx.send('Member needs an account to receive donations. {} make one now using `r.register`.'.format(member.mention))
        elif amount > self.pointmanager[str(ctx.author.id)]["points"]:
            await ctx.send('You cannot donate an amount you do not have.')
        else:
            self.pointmanager[str(ctx.author.id)]["points"]-=amount
            self.pointmanager[str(member.id)]["points"]+=amount
            self.save_settings()
            e = discord.Embed(color=ctx.author.color)
            e.set_author(name="{} received points from {}".format(member.name,ctx.author.name),icon_url=member.avatar_url_as(format=None))
            e.set_thumbnail(url=ctx.author.avatar_url_as(format=None))
            e.add_field(name='Amount Transferred', value='{} points'.format(amount), inline=False)
            e.add_field(name="{}'s new balance".format(ctx.author.name),
                        value="{} points".format(self.pointmanager[str(ctx.author.id)]["points"]), inline=False)
            e.add_field(name="{}'s new balance".format(member.name),
                        value="{} points".format(self.pointmanager[(str(member.id))]["points"]), inline=False)
            await ctx.send('{}, you just received {} points from {}! Put them to good use!'.format(member.mention,amount,
                           ctx.author.name),embed=e)

    @donate.error
    async def donate_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 21600, BucketType.user)
    async def points(self, ctx):
        number = random.randint(1, 40)
        if str(ctx.author.id) not in self.pointmanager:
            await ctx.send('{}, you do not have a registered points account. Make one now with `r.register`.'.format(ctx.author.mention))
        else:
            self.pointmanager[str(ctx.author.id)]["points"]+=number
            self.save_settings()
            e = discord.Embed(color=ctx.author.color)
            e.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url_as(format=None))
            e.set_thumbnail(url=ctx.author.avatar_url_as(format=None))
            e.add_field(name='Points Received',value='{} points'.format(number),inline=False)
            e.add_field(name='New Total', value='{} points'.format(self.pointmanager[str(ctx.author.id)]["points"],
                                                                   inline=False))
            await ctx.send(embed=e)

    @points.error
    async def points_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

def check_folders():
    if not os.path.exists("data/pointmanager"):
        print("Creating data/pointmanager folder...")
        os.makedirs("data/pointmanager")

def check_files():
    if not os.path.exists("data/pointmanager/pointmanager.json"):
        print("Creating data/pointmanager/pointmanager.json file...")
        dataIO.save_json("data/pointmanager/pointmanager.json", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Points(bot))