import discord
from discord.ext import commands

class miscFunctions():

    @classmethod
    async def displayImage(cls,ctx,imagePath,messageText=None):
        # await ctx.send(file=discord.file())
        if messageText is not None:
            await ctx.send(str(messageText),file = discord.File(imagePath))
        else:
            await ctx.send(file = discord.File(imagePath))