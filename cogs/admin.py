import discord
from discord.ext import commands

import datetime
import traceback


class Admin:
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send('Shutting down...')
        await self.bot.logout()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(embed=discord.Embed(color=ctx.message.author.color,
                                title = "⚠ Error",
                                description =f'```py\n{traceback.format_exc()}\n```'))
        else:
            await ctx.send(embed=discord.Embed(color=ctx.message.author.color,
                                title = "✅ Success",
                                description ="Plugin Loaded"))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send(embed=discord.Embed(color=ctx.message.author.color,
                                title = "⚠ Error",
                                description =f'```py\n{traceback.format_exc()}\n```'))
        else:
            await ctx.send(embed=discord.Embed(color=ctx.message.author.color,
                                title = "✅ Success",
                                description ="Plugin Unloaded"))


def setup(bot):
    bot.add_cog(Admin(bot))
