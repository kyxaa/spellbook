import discord
from discord.ext import commands
import random

class voiceMoveMemebers(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def privCon(self, ctx):
        membersInPrivCon = [ctx.author]
        if ctx.author.id == 158058710760030219:
            membersInPrivCon = []
            if hasattr(ctx.message,"mentions"):
                if len(ctx.message.mentions) > 0:
                    for member in ctx.message.mentions:
                        membersInPrivCon.append(member)
            if hasattr(ctx.author.voice,"channel"):
                for member in ctx.message.author.voice.channel.members:
                    if membersInPrivCon == []:
                        await ctx.send("You didn't specify anyone, sire.")
                    else:
                        if member in membersInPrivCon:
                            await member.move_to(discord.utils.get(ctx.guild.channels, id=696854070404579408))
                            # await member.send("A Private Conversation is being had. One moment please.")
                        else:
                            await member.send("The DM is having a Private Conversation. He'll be back....or at least I hope. I've rather enjoyed his company.")
            else:
                await ctx.send("You aren't in a voice channel, sire.")
        else:
            emojis = random.sample(ctx.bot.emojis,5)
            for emoji in emojis:
                await ctx.message.add_reaction(emoji)
            await ctx.send("Bitch, please.")

    @commands.command()
    async def endPrivCon(self, ctx):
        if ctx.author.id == 158058710760030219:
            for member in discord.utils.get(ctx.guild.channels, id=696854070404579408).members:
                await member.move_to(discord.utils.get(ctx.guild.channels, id=658080669640949793))

    @commands.command()
    async def disconnectAll(self, ctx):
        if ctx.author.id == 158058710760030219:
            if hasattr(ctx.author.voice,"channel"):
                    for member in ctx.message.author.voice.channel.members:
                        await member.move_to(None)

    @commands.command()
    async def connectUser(self, ctx):
        if ctx.author.id == 158058710760030219:
            if len(ctx.message.mentions) > 0:
                if hasattr(ctx.author.voice,"channel"):
                    for member in ctx.message.mentions:
                        await member.move_to(ctx.message.author.voice.channel)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.id == 158058710760030219:
            if hasattr(ctx.author.voice,"channel"):
                voiceChannel = ctx.author.voice.channel
                await voiceChannel.connect()
            else:
                await ctx.send("You aren't in a voice channel.")

    # @commands.command()
    # async def leave(ctx):
    #     if ctx.author.id == 158058710760030219:
    #         if hasattr(ctx.author.voice,"channel"):
    #             if ctx.me in ctx.author.voice.channel.memebers:

    #                 await voiceChannel.disconnect()
    #         else:
    #             await ctx.send("You aren't in a voice channel.")


def setup(bot):
    bot.add_cog(voiceMoveMemebers(bot))