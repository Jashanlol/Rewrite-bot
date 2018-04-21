import discord
from discord.ext import commands
import os

from .utils.dataIO import dataIO



class RoleManagement:
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
        await ctx.send("For {}, I can add role(s): {}".format(ctx.guild.name, rolemanager))

    @commands.command()
    async def roleconfigadd(self, ctx, role: discord.Role):
        if ctx.author is ctx.guild.owner:
            self.rolemanager[str(ctx.guild.id)] = role.id
            self.save_settings()
            await ctx.send("Role(s) saved")
        else:
            await ctx.send('Only server owner can you this command.')

    @commands.command()
    async def roleme(self, ctx, role: discord.Role):
        roles = discord.utils.get(ctx.guild.roles, id=self.rolemanager[(str(ctx.guild.id))])
        if self.rolemanager[(str(ctx.guild.id))] == role.id:
            await ctx.author.add_roles(roles)
        else:
            await ctx.send('You are not allowed to add that role.')

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
    bot.add_cog(RoleManagement(bot))
