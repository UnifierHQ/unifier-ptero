import discord
from discord.ext import commands

class Template(commands.Cog):
    """A template cog written for unifier-plugin temmplate repo"""
    
    def __init__(self,bot):
        self.bot = bot

    @commands.command
    async def template(self,ctx):
        await ctx.send('This is a template plugin!')

def setup(bot):
    bot.add_cog(Template(bot))
