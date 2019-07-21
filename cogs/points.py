import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

import os
import random
import asyncio
from .utils.dataIO import dataIO

class Points(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.pointmanager = dataIO.load_json("data/pointmanager/pointmanager.json")

    def save_settings(self):
        dataIO.save_json("data/pointmanager/pointmanager.json", self.pointmanager)

    @commands.command()
    async def horseinfo(self, ctx):
        await ctx.send('So you wanna play the horse game? So in this game, you bet money on a horse of your choice.'
                       'If your horse wins, you get money in proportion the percent chance of that horse winning.'
                       '\nAria has a 40% chance of winning\nBally has a 30% chance of winning\nBellagio has a '
                       '15% chance of winning\nFlamingo has a 10% chance of winning\nLuxor has a 5% chance of winning'
                       '\nNow that you have this information, use `r.horserace` to place your bet amount and which'
                       'horse you believe will win. ')

    @commands.command()
    async def horserace(self, ctx, amount: int, horse: str):
        list = 'Aria', 'Bally', 'Bellagio', 'Flamingo', 'Luxor'
        choices = random.choices(population=(list), weights=(40, 30, 15, 10, 5))
        choice = (choices[0])
        if choice != horse:
            Result = 'Defeat'
            result = 'lost'
            self.pointmanager[str(ctx.author.id)]['points'] -= amount
            points = amount
        else:
            Result = 'Victory'
            result = 'won'
            if horse == 'Aria':
                points = int(amount*0.5)
            if horse == 'Bally':
                points = int(amount)
            if horse == 'Bellagio':
                points = int(amount*1.5)
            if horse == 'Flamingo':
                points = int(amount*2)
            if horse == 'Luxor':
                points = int(amount*2.5)
            self.pointmanager[str(ctx.author.id)]['points']+=points
        self.save_settings()
        e = discord.Embed()
        e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
        e.add_field(name='Winner', value=choice)
        e.add_field(name='Your Choice', value=horse, inline=False)
        e.add_field(name=Result, value='You {} {} points'.format(result, points), inline=False)
        e.add_field(name='Overview', value='{} you now have {} points'.format(ctx.author.mention,
                                                                              self.pointmanager[str(ctx.author.id)]['points']))
        await ctx.send(embed=e)

    @horserace.error
    async def horserace_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    async def leaderboards(self, ctx):
        points_list = []
        for person_id, points_dict in self.pointmanager.items():
            points_list.append([person_id, points_dict["points"]])
        sorted_points_list = sorted(points_list, key=lambda x: x[1], reverse=True)
        string = ""
        for x in range(0,5):
            author = self.bot.get_user(int(sorted_points_list[x][0]))
            points = sorted_points_list[x][1]
            string += author.name + " " + str(points) + "\n"
            e = discord.Embed(title='Leaderboards',description=string, color=ctx.author.color)
        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
    @commands.guild_only()
    async def rob(self, ctx, *, member: discord.Member):
        choice = random.choice(['steal','safe','trolled'])
        amount = random.randint(1, 40)
        if str(ctx.author.id) not in self.pointmanager:
            await ctx.send('{} you do not have a points account. Make one using `r.register`.'.format(ctx.author.mention))
        elif choice == 'safe':
            await ctx.send('Robbery Failed! :frowning2:')
        elif choice == 'steal':
            if str(member.status) == 'online':
                await ctx.send('Who robs people while their home? Try again later!')
            else:
                if amount >= self.pointmanager[str(member.id)]["points"]:
                    await ctx.send("Cmon now! Who tries to steal from poor people! Up your game.")
                else:
                    self.pointmanager[str(ctx.author.id)]["points"]+=amount
                    self.pointmanager[str(member.id)]["points"]-=amount
                    self.save_settings()
                    e = discord.Embed(title='Robbery Results',color=ctx.author.color)
                    e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
                    e.set_thumbnail(url=ctx.author.avatar_url_as(format=None))
                    e.add_field(name='Robber', value='{} stole {} points'.format(ctx.author.name,amount),inline=False)
                    e.add_field(name='Victim',value='{} points were stolen from {}.'.format(amount,member.name),inline=False)
                    e.add_field(name='Overview', value="{} now has {} points\n{} now has {} points.".format(ctx.author.name,
                                                                                                            self.pointmanager[str(ctx.author.id)]["points"],
                                                                                                            member.name, self.pointmanager[str(member.id)]["points"]),inline=False)
                    await ctx.send(embed=e)
        elif choice == 'trolled':
            if str(member.status) == 'online':
                await ctx.send('Which idiot robs a house during the day.')
            elif self.pointmanager[str(ctx.author.id)]['secure'] is True:
                await ctx.send('Robbery Failed. :frowning2:')
            else:
                self.pointmanager[str(ctx.author.id)]["points"]-=amount
                self.pointmanager[str(member.id)]["points"]+=amount
                self.save_settings()
                e = discord.Embed(title='Woops...',color=member.color)
                e.set_author(name=member.name, icon_url=member.avatar_url_as(format=None))
                e.set_thumbnail(url=member.avatar_url_as(format=None))
                e.add_field(name='Robbery Backfired',value='{} stole '
                                                           '{} points from you while you were trying to rob them!'.format(member.name,amount))
                e.add_field(name='Overview', value='{} now has {} points\n{} now has {} points'.format(ctx.author.name,
                                                                                                       self.pointmanager[str(ctx.author.id)]["points"], member.name, self.pointmanager[str(member.id)]["points"]))
                e.set_footer(text="{}'s tip: Secure your house when you go to rob others!".format(self.bot.user.name),
                             icon_url=self.bot.user.avatar_url_as(format=None))
                await ctx.send(embed=e)

    @rob.error
    async def rob_handler(self,ctx,error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)


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
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    async def poker(self, ctx, amount:int, *, member:discord.Member):
        if amount is "0":
            await ctx.send('Seriously now?')
        elif str(ctx.author.id) not in self.pointmanager:
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
            await ctx.send("{} you have been challenged by {} in a game of poker for {} points! Do you y - accept or n - decline?"
                           "".format(member.mention, ctx.author.mention, amount))
            def check(m):
                return m.channel == ctx.channel and m.content in ['y','n'] and m.author == member
            msg = await self.bot.wait_for('message', check=check)
            if msg.content == "y":
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
            elif msg.content == 'n':
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
            self.pointmanager[str(ctx.author.id)] = {"points":0, "secure":False}
            self.save_settings()
            e=discord.Embed(color=ctx.author.color)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
            e.add_field(name="Points", value=self.pointmanager[str(ctx.author.id)]["points"])
            await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(rate=1,per=1.5,type=BucketType.user)
    async def slot(self, ctx):
        if self.pointmanager[str(ctx.author.id)]["points"] is 0:
            await ctx.send('Get some points!')
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
    @commands.cooldown(rate=1,per=2,type=BucketType.user)
    async def bet(self, ctx, amount:int):
        if amount is 0:
            await ctx.send('Seriously now?')
            return
        elif str(ctx.author.id) not in self.pointmanager:
            await ctx.send('{}, you need an account to gamble. Make one now with `r.register`.'.format(ctx.author.mention))
            return
        choice = random.choice(["won","lost"])
        if str(ctx.author.id) not in self.pointmanager:
            await ctx.send('You have no points.')
        elif amount <= self.pointmanager[str(ctx.author.id)]["points"]:
            if choice == "won":
                self.pointmanager[str(ctx.author.id)]["points"]+=amount
            elif choice == "lost":
                self.pointmanager[str(ctx.author.id)]["points"]-=amount
            points = self.pointmanager[str(ctx.author.id)]["points"]
            self.save_settings()
            e = discord.Embed(color=ctx.author.color)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
            e.add_field(name='Result',value="{} you {} {} points.".format(ctx.author.mention, choice,amount),inline=False)
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
            self.pointmanager[str(member.id)] = {"points":5, 'secure':False}
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
        if amount is 0:
            await ctx.send('Seriously now?')
        elif member is ctx.author:
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
            await ctx.send('You are on cooldown for {} seconds'.format(round(error.retry_after)))

    @commands.command()
    @commands.guild_only()
    async def secure(self, ctx):
        if str(ctx.author.id) not in self.pointmanager:
            await ctx.send('You are do not have a registered points account. Register now using`r.register`.')
        elif 0 >= self.pointmanager[str(ctx.author.id)]['points']:
            await ctx.send('You do not have enough points.')
        elif self.pointmanager[str(ctx.author.id)]['secure'] is True:
            await ctx.send('Account already secured!')
        else:
            self.pointmanager[str(ctx.author.id)]['secure'] = True
            self.pointmanager[str(ctx.author.id)]['points']-=30
            self.save_settings()
            e = discord.Embed(title='Receipt', color=ctx.author.color)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
            e.add_field(name='Charged', value='30 points', inline=False)
            e.add_field(name='Hours', value='House secure for 6 hours.')
            e.add_field(name='Overview', value='{} you now have {} points.'.format(ctx.author.mention,
                                                                                   self.pointmanager[
                                                                                       str(ctx.author.id)]['points']),inline=False)
            await ctx.send(embed=e)
            x = 1
            while True:
                x+=1
                await asyncio.sleep(21600)
                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author
                await ctx.send(' {} would you like to continue security? y - yes, n - no'.format(ctx.author.mention))
                msg = await self.bot.wait_for('message', check=check)
                if msg.content == 'y':
                    self.pointmanager[str(ctx.author.id)]['secure'] = True
                    self.pointmanager[str(ctx.author.id)]['points'] -= 30
                    self.save_settings()
                    f = discord.Embed(title='Receipt', color=ctx.author.color)
                    f.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format=None))
                    f.add_field(name='Charged', value='1 points', inline=False)
                    f.add_field(name='Hours', value='House secure for 6 hours.')
                    f.add_field(name='Overview', value='{} you now have {} points.'.format(ctx.author.mention,
                    self.pointmanager[
                    str(ctx.author.id)][
                    'points']),inline=False)
                    await ctx.send(embed=f)
                if msg.content == 'n':
                    await ctx.send('Security canceled. :frowning2:')
                    self.pointmanager[str(ctx.author.id)]['secure'] = False
                    self.save_settings()
                    return

    @secure.error
    async def secure_handler(self, ctx, error):
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