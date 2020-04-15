import discord
from discord.ext import commands
# this can be used to define channel specific

class guildSpecific(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.guildId= 0 #replace 0 with the guild ID

    @commands.command()
    async def guildSpecificFunction(self,ctx):
        if ctx.guild.id == self.guildId:
            pass  #logic here


def setup(bot):
    bot.add_cog(guildSpecific(bot))