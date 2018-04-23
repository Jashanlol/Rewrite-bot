import discord
from discord.ext import commands
import os
import datetime

from .utils.dataIO import dataIO


class StarManager:
    def __init__(self, bot):
        self.bot = bot
        self.starmanager = dataIO.load_json("data/starmanager/starmanager.json")


    def save_settings(self):
        dataIO.save_json("data/starmanager/starmanager.json", self.starmanager)

    @commands.command()
    async def setupstars(self, ctx, channel: discord.TextChannel):
        if ctx.author is ctx.guild.owner:
            if str(ctx.guild.id) in self.starmanager:
                self.starmanager[(str(ctx.guild.id))].append(channel.id)
            else:
                self.starmanager[(str(ctx.guild.id))] = [channel.id]
            self.save_settings()
            await ctx.end('Channel saved.')
        else:
            await ctx.send('Only the server can setupstars channnel.')

    async def on_reaction_add(self, reaction, user):
        if reaction.emoji is not '⭐':
            return
        if reaction.message.id in self.starmanager[str(reaction.message.guild.id)]:
            star_channel.get_message(stars[str(reaction.message.guild.id)][str(reaction.message.id)].edit(+1))
        else:
            e = discord.Embed(description=reaction.message.content)
            e.set_author(name=reaction.message.author, icon_url=reaction.message.avatar_url_as(format=None))
            e.timestamp = datetime.datetime.utcnow()
            self.starmanager[str(reaction.message.guild.id)].append(reaction.message.id)
            if str(reaction.message.guild.id) in self.starmanager:
                channel = self.starmanager[str(reaction.message.guild.id)]
            else:
                await reaction.message.send('Star channel not setup yet. Use `r.setupstars` to setup now.')
            await channel.send(embed=e)

def check_folders():
    if not os.path.exists("data/starmanager"):
        print("Creating data/starmanager folder...")
        os.makedirs("data/starmanager")


def check_files():
    if not os.path.exists("data/starmanager/starmanager.json"):
        print("Creating data/starmanager/starmanager.json file...")
        dataIO.save_json("data/starmanager/starmanager.json", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(StarManager(bot))
