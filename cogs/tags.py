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

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, name: str):
        if str(ctx.guild.id) in self.tagmanager:
            if name in self.tagmanager[str(ctx.guild.id)]:
                await ctx.send(self.tagmanager[str(ctx.guild.id)][name]["value"])
            else:
                await ctx.send("Tag not found.")
        else:
                await ctx.send("This guild has no tags.")

    @tag.command()
    async def create(self, ctx, name: str, *, value: str):
        if name == 'tag':
            await ctx.send('This tag name starts with a reserved word.')
            return
        elif name == 'delete':
            await ctx.send('This tag name starts with a reserved word.')
            return
        elif name == 'create':
            await ctx.send('This tag name starts with a reserved word.')
            return
        elif name == 'box':
            await ctx.send('This tag name starts with a reserved word.')
            return
        elif str(ctx.guild.id) in self.tagmanager:
            self.tagmanager[(str(ctx.guild.id))][name] = {"value" : value, "author_id" : ctx.author.id}
        else:
            self.tagmanager[(str(ctx.guild.id))] = {name : {"value" : value, "author_id" : ctx.author.id}}
        self.save_settings()
        await ctx.send('Tag created.')

    @tag.command()
    async def delete(self, ctx, name: str):
        if name == 'tag':
            await ctx.send('This tag name starts with a reserved word.')
            return
        elif name == 'delete':
            await ctx.send('This tag name starts with a reserved word.')
            return
        elif name == 'create':
            await ctx.send('This tag name starts with a reserved word.')
            return
        elif name == 'box':
            await ctx.send('This tag name starts with a reserved word.')
            return
        elif str(ctx.guild.id) in self.tagmanager:
            if name in self.tagmanager[str(ctx.guild.id)]:
                if self.tagmanager[str(ctx.guild.id)][name]["author_id"] == ctx.author.id:
                    self.tagmanager[str(ctx.guild.id)].pop(name)
                else:
                    await ctx.send("You are not the owner of this tag.")
                    return
            else:
                await ctx.send("This guild has no tags.")
                return
            self.save_settings()
            await ctx.send('Tag removed.')
        else:
            await ctx.send('Cannot delete this.')

    @tag.command()
    async def box(self, ctx):
        if str(ctx.guild.id) in self.tagmanager:
            if self.tagmanager[(str(ctx.guild.id))]:
                e = discord.Embed(title='Server tags:',
                                  description="\n".join(key for key in self.tagmanager[str(ctx.guild.id)].keys()))
                await ctx.send(embed=e)
        else:
            await ctx.send('No tags. :frowning2:')


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
