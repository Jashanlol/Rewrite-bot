import datetime
import os

import discord
from discord.ext import commands

from .utils.dataIO import dataIO


class StarManager:
    def __init__(self, bot):
        self.bot = bot
        self.starchannel = dataIO.load_json("data/starchannel/starchannel.json")

    def save_settings(self):
        dataIO.save_json("data/starchannel/starchannel.json", self.starchannel)

    @commands.group(invoke_without_command=True)
    async def star(self, ctx):
        return

    @star.command()
    async def setup(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            await ctx.send('Channel is required.')
        if ctx.author is ctx.guild.owner:
            self.starchannel[(str(ctx.guild.id))] = {"channel": channel.id, "starred_messages" : {}}
            self.save_settings()
            await ctx.send('Channel saved.')
        else:
            await ctx.send('Only the server can setup stars channel.')

    @star.command()
    async def channel(self, ctx):
        if str(ctx.guild.id) in self.starchannel:
            channel = self.bot.get_channel(self.starchannel[(str(ctx.guild.id))]["channel"])
            if not channel:
                await ctx.send("Star channel has been deleted")
            else:
                await ctx.send('Stars channel is {}'.format(channel.mention))
        else:
            await ctx.send('Stars channel is not setup. Setup now with `r.setupstars`.')

    @star.command()
    async def show(self, ctx, id):
        guild_id = str(ctx.guild.id)
        guild_stars_settings = self.starchannel[guild_id]
        star_channel_id = guild_stars_settings["channel"]
        star_channel = discord.utils.get(ctx.guild.channels, id=star_channel_id)
        if id in guild_stars_settings["starred_messages"]:
            starboard_message_id = guild_stars_settings["starred_messages"][str(id)][
                "starboard_message_id"]
            starboard_messages = await star_channel.history(limit=1000).flatten()
            starboard_message = discord.utils.get(starboard_messages, id=starboard_message_id)
            if not starboard_message:
                return
            embeds = starboard_message.embeds[0]
            await ctx.send(starboard_message.content,embed=embeds)
        else:
            await ctx.send('Message not found in star channel.')

    async def on_reaction_add(self, reaction, user):
        if reaction.emoji != '⭐':
            return
        if reaction.count >= 2:
            guild_id = str(reaction.message.guild.id)
            message_id = str(reaction.message.id)
            if guild_id not in self.starchannel:
                return
            else:
                guild_stars_settings = self.starchannel[guild_id]
            star_channel_id = guild_stars_settings["channel"]
            star_channel = discord.utils.get(reaction.message.guild.channels, id=star_channel_id)
            if not star_channel:
                return
            e = discord.Embed(description=reaction.message.content, color=0xeac90f)
            e.timestamp = datetime.datetime.utcnow()
            e.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url_as(format=None))
            if str(reaction.message.id) in guild_stars_settings["starred_messages"]:
                starboard_message_id = guild_stars_settings["starred_messages"][str(reaction.message.id)]["starboard_message_id"]
                starboard_messages = await star_channel.history(limit=1000).flatten()
                starboard_message = discord.utils.get(starboard_messages, id=starboard_message_id)
                if not starboard_message:
                    return
                guild_stars_settings["starred_messages"][message_id]["stars"] +=1
                if reaction.count >= 5:
                    await starboard_message.edit(content="🌟 " + "**" + str(reaction.count)
                                                         + "**  " + reaction.message.channel.mention
                                + "  ID: " + str(reaction.message.id), embed=e)
                    if reaction.count >= 10:
                        await starboard_message.edit(content="💫 " + "**" + str(reaction.count) + "**  "
                                                             + reaction.message.channel.mention
                                    + "  ID: " + str(reaction.message.id), embed=e)
                        if reaction.count >= 25:
                            await starboard_message.edit(content="✨ " + "**" + str(reaction.count)
                                                                 + "**  " + reaction.message.channel.mention
                                        + "  ID: " + str(reaction.message.id), embed=e)
                    else:
                        await starboard_message.edit(content="⭐ " + "**" + str(reaction.count) + "**  "
                                                             + reaction.message.channel.mention
                                                             + "  ID: " + str(reaction.message.id), embed=e)
            else:
                msg = await star_channel.send("⭐ " +"**"+str(reaction.count)+"**  "  + reaction.message.channel.mention
                                           + "  ID: " + str(reaction.message.id),embed=e)
                guild_stars_settings["starred_messages"][message_id] = {"starboard_message_id" : msg.id, "stars" : 1}
            self.save_settings()
        else:
            await reaction.message.channel.send('Star channel not setup. Setup now using `r.star setup`.')

    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji != '⭐':
            return
        guild_id = str(reaction.message.guild.id)
        message_id = str(reaction.message.id)
        if guild_id not in self.starchannel:
            return
        else:
            guild_stars_settings = self.starchannel[guild_id]
        star_channel_id = guild_stars_settings["channel"]
        star_channel = discord.utils.get(reaction.message.guild.channels, id=star_channel_id)
        if not star_channel:
            return
        e = discord.Embed(description=reaction.message.content, color=0xeac90f)
        e.timestamp = datetime.datetime.utcnow()
        e.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url_as(format=None))
        if str(reaction.message.id) in guild_stars_settings["starred_messages"]:
            starboard_message_id = guild_stars_settings["starred_messages"][str(reaction.message.id)][
                "starboard_message_id"]
            starboard_messages = await star_channel.history(limit=1000).flatten()
            starboard_message = discord.utils.get(starboard_messages, id=starboard_message_id)
            if not starboard_message:
                return
            guild_stars_settings["starred_messages"][message_id]["stars"] -=1
            if reaction.count >= 5:
                await starboard_message.edit(content="🌟 " + "**" + str(reaction.count)
                                                     + "**  " + reaction.message.channel.mention
                                                     + "  ID: " + str(reaction.message.id), embed=e)
                if reaction.count >= 10:
                    await starboard_message.edit(content="💫 " + "**" + str(reaction.count) + "**  "
                                                         + reaction.message.channel.mention
                                                         + "  ID: " + str(reaction.message.id), embed=e)
                    if reaction.count >= 25:
                        await starboard_message.edit(content="✨ " + "**" + str(reaction.count)
                                                             + "**  " + reaction.message.channel.mention
                                                             + "  ID: " + str(reaction.message.id), embed=e)
            else:
                await starboard_message.edit(content="⭐ " + "**" + str(reaction.count) + "**  "
                                                     + reaction.message.channel.mention
                                                     + "  ID: " + str(reaction.message.id), embed=e)
            self.save_settings()


def check_folders():
    if not os.path.exists("data/starchannel"):
        print("Creating data/starchannel folder...")
        os.makedirs("data/starchannel")

def check_files():
    if not os.path.exists("data/starchannel/starchannel.json"):
        print("Creating data/starchannel/starchannel.json file...")
        dataIO.save_json("data/starchannel/starchannel.json", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(StarManager(bot))
