import discord
from discord.ext import commands
from miscFunctions import miscFunctions
# Example of how to build out the fucntions in this file:
    # class guildSpecific(commands.Cog):
    #     def __init__(self,bot):
    #         self.bot = bot
    #         self.guildId= 0 #replace 0 with the guild ID

    #     @commands.command()
    #     async def guildSpecificFunction(self,ctx):
    #         if ctx.guild.id == self.guildId:
    #             pass #logic here
# You can add as many classes you want that will be guild specific. Be sure to include them into the "setup" function or the bot won't use it.
class dsNDs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.guildId= 658080668886237194 #replace 0 with the guild ID

    @commands.command()
    async def displayMap(self,ctx):
        if ctx.guild.id == self.guildId:
            await miscFunctions.displayImage(ctx,"swordCoast.png",messageText="Here is your map: ")

    @commands.command()
    async def display_members(self,ctx:commands.Context):
        if ctx.guild.id == self.guildId:
            member_list = "Members of this guild:"
            for member in ctx.guild.members:
                member_list += f"\n{member.name}    {member.id}"
            await ctx.send(content=member_list)

def setup(bot):
    bot.add_cog(dsNDs(bot))