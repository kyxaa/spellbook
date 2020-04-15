import discord
from discord.ext import commands

class miscFunctions():

    # @commands.Cog.listener()
    # async def on_ready(self):
        # await def on_raw_reaction_add(self,payload):
        #     if payload.emoji.id == 697266516709605447 and payload.user_id == 158058710760030219:
        #         message = await self.bot.fetch_message(payload.message_id)

    async def displayImage(self,ctx,imagePath):
        ctx.send(file="swordCoast.png")