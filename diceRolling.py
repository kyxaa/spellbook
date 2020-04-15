import discord
from discord.ext import commands
import math
import random
import re
import pandas as pd
import fuckWithPeople
import loggingAndErrors

class diceRolling:

    @classmethod
    def roll(self, arg: str):
        inputs = arg.split("+")
        resultsDict = {
            "Input":[],
            "Rolls":[],
            "Total":[],
    }
        if self.validateInput(inputs):
            for input in inputs:
                modifiers =  re.findall(r"^[0-9]+$",input) + re.findall(r"\-[0-9]+",input)
                for modifier in modifiers:
                    input = re.sub(modifier,"",input)
                regex = re.match(r"^([0-9]+)?(d([0-9]+))?$",input.lower())
                rollResults = []
                if regex is not None and not regex[0] == "":
                    resultsDict["Input"].append(regex[0])
                    if regex[1] is None:
                        numOfDice = 1
                    else:
                        numOfDice = int(regex[1])
                    if regex[2] is None:
                        typeOfDice = 1
                    else:
                        typeOfDice = int(regex[3])
                    i=1
                    while i <= numOfDice:
                        random.seed()
                        rollResults.append(random.randint(1,typeOfDice))
                        i += 1
                    resultsDict["Rolls"].append(rollResults)
                    resultsDict["Total"].append(sum(rollResults))
                for modifier in modifiers:
                    resultsDict["Input"].append(modifier)
                    resultsDict["Rolls"].append([int(modifier)])
                    resultsDict["Total"].append(int(modifier))
            return resultsDict

    @classmethod
    def validateInput(self, splitList: list):
        for roll in splitList:
            match = re.match("^(-?[0-9]+)?(d([0-9]+))?(-[0-9]+)?$",roll)
            if match is None:
                return False
        return True
    @classmethod
    def display(self, rollResults: dict):
        if rollResults is not None:
            df = pd.DataFrame(rollResults)
            total = sum(rollResults['Total'])
            if total < 0:
                totalStr = f"**NEGATIVE** {fuckWithPeople.replaceCharactersWithEmojis(str(total*-1))}"
            else:
                totalStr = fuckWithPeople.replaceCharactersWithEmojis(str(total))
            return f"The result of your roll is:\n```{df.to_string(index=False)}```\nWhich brings us to a grand total of {totalStr}!!!"
        else:
            return "The input for this roll wasn't correct. Please try again."

    @classmethod
    def rollDisplay(self, input: str):
        return self.display(self.roll(input))


class diceRollingCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def roll(self,ctx,*,input: str):
        input = input.replace(" ","")
        response = diceRolling.rollDisplay(input)
        responseList = [response]
        await ctx.send(response)
        loggingAndErrors.writeToLogs(ctx,responseList)

def setup(bot):
    bot.add_cog(diceRollingCog(bot))