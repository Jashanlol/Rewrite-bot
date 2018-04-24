import discord
from discord.ext import commands
import os
import datetime

from .utils.dataIO import dataIO


class StarManager:
    def __init__(self, bot):
        self.bot = bot
        self.starchannel = dataIO.load_json("data/starchannel/starchannel.json")
        self.starmanager = dataIO.load_json("data/starmanager/starmanager.json")

    def save_settings(self):
        dataIO.save_json("data/starchannel/starchannel.json", self.starchannel)
        dataIO.save_json("data/starmanager/starmanager.json", self.starmanager)


    @commands.command()
    async def setupstars(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            await ctx.send('Channel is required.')
        if ctx.author is ctx.guild.owner:
            self.starchannel[(str(ctx.guild.id))] = {"channel": channel.id, "starred_messages" : {}}
            self.save_settings()
            await ctx.send('Channel saved.')
        else:
            await ctx.send('Only the server can setup stars channel.')

    @commands.command()
    async def starschannel(self, ctx):
        if str(ctx.guild.id) in self.starchannel:
            channel = self.bot.get_channel(self.starchannel[(str(ctx.guild.id))]["channel"])
            if not channel:
                await ctx.send("Star channel has been deleted")
            else:
                await ctx.send('Stars channel is {}'.format(channel.mention))
        else:
            await ctx.send('Stars channel is not setup. Setup now with `r.setupstars`.')

    async def on_reaction_add(self, reaction, user):
        if reaction.emoji != '⭐':
            return

        guild_id = str(reaction.message.guild.id)
        message_id = str(reaction.message.id)
        if guild_id not in self.starmanager:
            return
        else:
            guild_stars_settings = self.starmanager[guild_id]

        star_channel_id = guild_stars_settings["channel"]
        star_channel = self.bot.get_channel(star_channel_id)
        if not channel:
            return

       if message_id in guild_stars_settings["starred_messages"]:
           starboard_message_id = guild_stars_settings["starred_messages"][message_id]["starboard_message_id"]
           starboard_message = starchannel.get_message(starboard_message_id)
           if not starboard_message:
               return
           guild_start_setting["starred_messages"][message_id]["stars"] += 1
           stars = guild_start_setting["starred_messages"][message_id]["stars"]
           await starboard_message.edit(INSERT YOUR EDITED MESSAGE HERE)
       else:
           msg = await starchannel.send(INSERT NEW STAR MESSAGE HERE)
           guild_stars_settings["starred_messages"][message_id] = {"starboard_message_id" : msg.id, "stars" : 1}
       
       self.starmanager[guild_id] = guild_stars_settings
       self.save_settings


def check_folders():
    if not os.path.exists("data/starmanager"):
        print("Creating data/starmanager folder...")
        os.makedirs("data/starmanager")

    if not os.path.exists("data/starchannel"):
        print("Creating data/starchannel folder...")
        os.makedirs("data/starchannel")

def check_files():
    if not os.path.exists("data/starmanager/starmanager.json"):
        print("Creating data/starmanager/starmanager.json file...")
        dataIO.save_json("data/starmanager/starmanager.json", {})

    if not os.path.exists("data/starchannel/starchannel.json"):
        print("Creating data/starchannel/starchannel.json file...")
        dataIO.save_json("data/starchannel/starchannel.json", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(StarManager(bot))
