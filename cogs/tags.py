import discord
from discord.ext import commands
import os

from .utils.dataIO import dataIO

class Tags:
    def __init__(self, bot):
        self.bot = bot
        self.tagmanager = dataIO.load_json("data/tagmanager/tagmanager.json")


    def save_settings(self):
        dataIO.save_json("data/tagmanager/tagmanager.json", self.tagmanager)

    @commands.command()
    async def create_tag(self, ctx, name: str, *, value: str):
        if str(ctx.guild.id) in self.tagmanager:
            self.tagmanager[(str(ctx.guild.id)) + name].append(value)
        else:
            self.tagmanager[(str(ctx.guild.id)) + name] = (value)
        self.save_settings()
        await ctx.send('Tag created.')

    @commands.command()
    async def delete_tag(self, ctx, name: str):
        if [(str(ctx.guild.id)) + name] in self.tagmanager:
            self.tagmanager[(str(ctx.guild.id))].remove[(str(ctx.guild.id)) + name]
        await ctx.send('Tag removed.')

    @commands.command()
    async def tag(self, ctx, name: str):
        if str(ctx.guild.id) in self.tagmanager:
            tagmanager = self.tagmanager[(str(ctx.guild.id)) + name]
            await ctx.send('{}',(tagmanager))

def check_folders():
    if not os.path.exists("data/tagmanager"):
        print("Creating data/tagmanager folder...")
        os.makedirs("data/tagmanager")


def check_files():
    if not os.path.exists("data/tagmanager/tagmanager.json"):
        print("Creating data/tagmanager/tagmanager.json file...")
        dataIO.save_json("data/tagmanager/tagmanager.json", {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Tags(bot))
