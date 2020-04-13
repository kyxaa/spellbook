# import requests
import discord
import os
from dotenv import load_dotenv
import pandas as pd
# import asyncio
# import re
# import spells
# import sqlite3
from discord.ext import commands
# ,owner_id='658080668886237194'
from config import invocation
bot = commands.Bot(command_prefix=invocation)

# import logging
# from datetime import datetime
# import random
import voiceAudio
import voiceMoveMembers
import fuckWithPeople
import dndSpells
import diceRolling

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

# logging.basicConfig(
#     filename='logs.log',
#     format='<%(asctime)s> %(levelname)-8s %(message)s',
#     level=logging.INFO,
#     datefmt='%Y-%m-%d %H:%M:%S')

# LOCAL FUNCTIONS

# def convertLongResponseToArray(response):
#     retVal = []
#     while len(response) > 1999:
#         retVal.append(response[0:1999])
#         response = response[1999:]
#     retVal.append(response)
#     return retVal

# def convertLongResponseWithLinesToArray(response):
#     retVal = []
#     tempList = response.split("\n")
#     i = 0
#     beginString = 0
#     numberofCharacters = 0
#     for string in tempList:
#         numberofCharacters = numberofCharacters + len(string)
#         if numberofCharacters > 1850:
#             listItem = '\n'.join(tempList[beginString:i+1]) + "\n"
#             retVal.append(listItem)
#             beginString = i + 1
#             numberofCharacters = 0
#         if string == tempList[-1]:
#             if not tempList[beginString:] == []:
#                 retVal.append('\n'.join(tempList[beginString:]))
#         i += 1
#     return retVal


# def writeToLogs(ctx,responseList):
#     responseText = ""
#     if hasattr(ctx.channel, "name"):
#         channelName = ctx.channel.name
#     else:
#         channelName = "Direct Message"
#     if ctx.guild is not None:
#         guildName = ctx.guild.name
#     else:
#         guildName = "Not Applicable"
#     for response in responseList:
#         responseText = responseText + response
#     logInfo = f"Activity Detected\n\
#     USERNAME: {ctx.author.name}\n\
#     CHANNEL: {channelName}\n\
#     SERVER: {guildName}\n\
#     REQUEST: {ctx.message.content}\n"
#     print(f"<{datetime.now()}>: {logInfo}RESPONSE:\n{responseText[:100]}")
#     logging.info(f"{logInfo}RESPONSE:\n{responseText}")


# def randomAnimatedEmoji(ctx, numberOfEmojis):
#     animatedEmojis = []
#     if numberOfEmojis > len(ctx.bot.emojis):
#         numberOfEmojis = len(ctx.bot.emojis)
#     for emoji in ctx.bot.emojis:
#         if emoji.animated:
#             animatedEmojis.append(emoji)
#     animatedEmojis = random.sample(animatedEmojis,numberOfEmojis)
#     return animatedEmojis




# EVENTS

@bot.event
async def on_ready():
    print("Connecting to Guilds...")
    guildsDisplay = {
        "Guild Name":[],
        "Total Memebers":[],
        "Members Online":[],
    }
    
    for guild in bot.guilds:
        membersOnline = 0
        guildsDisplay["Guild Name"].append(guild.name)
        guildsDisplay["Total Memebers"].append(len(guild.members))
        for member in guild.members:
            if member.status.name == "online":
                membersOnline += 1
        guildsDisplay["Members Online"].append(membersOnline)
    
    df = pd.DataFrame(guildsDisplay)

    print(df.to_string(index=False))

# @bot.event
# async def on_message(message):
# pass

# COMMANDS

# @bot.command()
# async def spell(ctx, arg):
#     responseList = []
#     if ctx.message.author.id == 695782503759478794:
#         messageForKillBot = "Really? You think that will work?"
#         await ctx.send(messageForKillBot)
#         responseList.append(messageForKillBot)
#     else:
#         spellName = re.sub(r"!spell[\s]*", "", ctx.message.content.lower())
#         spellInfo = spells.displaySpell(spellName)
#         if spellInfo is not None:
#             if len(spellInfo) > 1999:
#                 responseList = convertLongResponseToArray(spellInfo)
#             else:
#                 responseList.append(spellInfo)
#             for response in responseList:
#                 await ctx.send(response)
#         else:
#             responseList.append("Make sure you spelled your spell name correctly. The format for that command is \n```!spell [name of spell]```")
#             for response in responseList:
#                 await ctx.send(response)
#     if not responseList == []:
#         for emoji in fuckWithPeople.randomAnimatedEmoji(ctx,5):
#             await ctx.message.add_reaction(emoji)
#         writeToLogs(ctx,responseList)

# @bot.command()
# async def spellList(ctx, arg):
#     responseList = []
#     if ctx.message.author.id == 695782503759478794:
#         messageForKillBot = "Really, Killbot?? Do you think I'll be defeated that easily?????"
#         await ctx.send(messageForKillBot)
#         responseList.append(messageForKillBot)
#     else:
#         spellClass = re.sub(r"!spelllist[\s]*", "", ctx.message.content.lower())
#         spellList = spells.displaySpellList(spellClass)
#         if spellList is not None:
#             if len(spellList) > 1999:
#                 responseList = convertLongResponseWithLinesToArray(spellList)
#             else:
#                 responseList.append(spellList)
#             for response in responseList:
#                 if response == responseList[0]:
#                     await ctx.send(f"__**{spellClass.title()} Spells**__\n```{response}```")
#                 else:
#                     await ctx.send(f"```{response}```")
#         else:
#             responseList.append("Make sure you spelled the class name correctly. The format for that command is\n```!spelllist [class]```")
#             for response in responseList:
#                 await ctx.send(response)
#         if not responseList == []:
#             for emoji in fuckWithPeople.randomAnimatedEmoji(ctx,5):
#                 await ctx.message.add_reaction(emoji)
#             writeToLogs(ctx,responseList)

diceRolling.setup(bot)
voiceAudio.setup(bot)
voiceMoveMembers.setup(bot)
fuckWithPeople.setup(bot)
dndSpells.setup(bot)
bot.run(discord_token)