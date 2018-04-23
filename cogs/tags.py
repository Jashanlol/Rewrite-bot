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
    async def delete(self, ctx, tag, *, name: str):
        if tag == 'tag':
            if str(ctx.guild.id) in self.tagmanager:
                if name in self.tagmanager[str(ctx.guild.id)]:
                    self.tagmanager[str(ctx.guild.id)].pop(name)
                else:
                    await ctx.send("Tag not found.")

    async def create_tag(self, ctx, name: str, *, value: str):
        if str(ctx.guild.id) in self.tagmanager:
            self.tagmanager[(str(ctx.guild.id))][name] = {"value" : value, "author_id" : ctx.author.id}
        else:
            self.tagmanager[(str(ctx.guild.id))] = {name : {"value" : value, "author_id" : ctx.author.id}} 
        self.save_settings()
        await ctx.send('Tag created.')

    @commands.command()
    async def delete_tag(self, ctx, name: str):
        if str(ctx.guild.id)  in self.tagmanager:
            if name in self.tagmanager[str(ctx.guild.id)]:
                if self.tagmanager[str(ctx.guild.id)][name]["author_id"] == ctx.author.id
                    self.tagmanager[str(ctx.guild.id)].pop(name)
                else:
                    await ctx.send("You are not the owner of this tag")
                    return
            else:
                await ctx.send("This guild has no tags.")
                return
            self.save_settings()
            await ctx.send('Tag removed.')
        else:
            await ctx.send('Cannot delete this.')

    @commands.command()
    async def tag(self, ctx, *, name: str):
        if name == 'box':
            if str(ctx.guild.id) in self.tagmanager:
                if self.tagmanager[(str(ctx.guild.id))]:
                    e = discord.Embed(title='Server tags:',
                                      description="\n".join(key for key in self.tagmanager[str(ctx.guild.id)].keys()))
                    await ctx.send(embed=e)
            else:
                await ctx.send('No tags :frowning2:')
        else:
            if str(ctx.guild.id) in self.tagmanager:
                if name in self.tagmanager[str(ctx.guild.id)]:
                    await ctx.send(self.tagmanager[str(ctx.guild.id)][name])
                else:
                    await ctx.send("Tag not found.")
            else:
                await ctx.send("This guild has no tags.")


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
