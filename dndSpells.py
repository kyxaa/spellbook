import discord
from discord.ext import commands
import spells
import re
import fuckWithPeople
import loggingAndErrors

def convertLongResponseToArray(response):
    retVal = []
    while len(response) > 1999:
        retVal.append(response[0:1999])
        response = response[1999:]
    retVal.append(response)
    return retVal

def convertLongResponseWithLinesToArray(response):
    retVal = []
    tempList = response.split("\n")
    i = 0
    beginString = 0
    numberofCharacters = 0
    for string in tempList:
        numberofCharacters = numberofCharacters + len(string)
        if numberofCharacters > 1850:
            listItem = '\n'.join(tempList[beginString:i+1]) + "\n"
            retVal.append(listItem)
            beginString = i + 1
            numberofCharacters = 0
        if string == tempList[-1]:
            if not tempList[beginString:] == []:
                retVal.append('\n'.join(tempList[beginString:]))
        i += 1
    return retVal

class dndSpells(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def spell(self, ctx, arg):
        responseList = []
        if ctx.message.author.id == 695782503759478794:
            messageForKillBot = "Really? You think that will work?"
            await ctx.send(messageForKillBot)
            responseList.append(messageForKillBot)
        else:
            spellName = re.sub(r"!spell[\s]*", "", ctx.message.content.lower())
            spellInfo = spells.displaySpell(spellName)
            if spellInfo is not None:
                if len(spellInfo) > 1999:
                    responseList = convertLongResponseToArray(spellInfo)
                else:
                    responseList.append(spellInfo)
                for response in responseList:
                    await ctx.send(response)
            else:
                responseList.append("Make sure you spelled your spell name correctly. The format for that command is \n```!spell [name of spell]```")
                for response in responseList:
                    await ctx.send(response)
        if not responseList == []:
            for emoji in fuckWithPeople.randomAnimatedEmoji(ctx,5):
                await ctx.message.add_reaction(emoji)
            loggingAndErrors.writeToLogs(ctx,responseList)

    @commands.command()
    async def spellList(self, ctx, arg):
        responseList = []
        if ctx.message.author.id == 695782503759478794:
            messageForKillBot = "Really, Killbot?? Do you think I'll be defeated that easily?????"
            await ctx.send(messageForKillBot)
            responseList.append(messageForKillBot)
        else:
            spellClass = re.sub(r"!spelllist[\s]*", "", ctx.message.content.lower())
            spellList = spells.displaySpellList(spellClass)
            if spellList is not None:
                if len(spellList) > 1999:
                    responseList = convertLongResponseWithLinesToArray(spellList)
                else:
                    responseList.append(spellList)
                for response in responseList:
                    if response == responseList[0]:
                        await ctx.send(f"__**{spellClass.title()} Spells**__\n```{response}```")
                    else:
                        await ctx.send(f"```{response}```")
            else:
                responseList.append("Make sure you spelled the class name correctly. The format for that command is\n```!spelllist [class]```")
                for response in responseList:
                    await ctx.send(response)
            if not responseList == []:
                for emoji in fuckWithPeople.randomAnimatedEmoji(ctx,5):
                    await ctx.message.add_reaction(emoji)
                loggingAndErrors.writeToLogs(ctx,responseList)

def setup(bot):
    bot.add_cog(dndSpells(bot))