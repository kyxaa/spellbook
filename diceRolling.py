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
        for input in inputs:
            negativeModifier = re.findall(r"\-[0-9]*",input)
            if not negativeModifier == []:
                # negativeModifierStr = negativeModifier[0]
                newInput = re.sub(negativeModifier[0],"",input)
            else:
                newInput = input
            regex = re.match(r"^([0-9]*)?(d([0-9]*))?$",newInput.lower())
            rollResults = []
            justANumber = False
            #TODO: Add handling for bad input
            if regex is not None and not regex[0] == "":
                resultsDict["Input"].append(regex[0])
                if regex[1] == "":
                    numOfDice = 1
                else:
                    numOfDice = int(regex[1])
                if regex[2] is None:
                    justANumber = True
                else:
                    typeOfDice = int(regex[3])
                i=1
                if not justANumber:
                    while i <= numOfDice: 
                        random.seed()
                        rollResults.append(random.randint(1,typeOfDice))
                        i += 1
                else:
                    rollResults.append(numOfDice)
                resultsDict["Rolls"].append(rollResults)
                resultsDict["Total"].append(sum(rollResults))
                if not negativeModifier == []:
                    resultsDict["Input"].append(negativeModifier[0])
                    resultsDict["Rolls"].append([int(negativeModifier[0])])
                    resultsDict["Total"].append(int(negativeModifier[0]))
        return resultsDict

    @classmethod
    def display(self, rollResults: dict):
        # displayStr = ""
        # thingsToBeAdded = []
        # for key in rollResults.keys():
        #     try:
        #         key = int(key)
        #         thingsToBeAdded.append(key)
        #     except:
        #         displayStr = f"{displayStr}**{key.upper()}**:{rollResults[key]}\n"
        #         thingsToBeAdded.append(sum(rollResults[key]))
        # # thingsToBeAdded = str(' + '.join([sum(rolls[rolls]) for rolls in rollResults.keys()]))
        # # rollTotal = sum([sum(rolls[rolls]) for rolls in rollResults.keys()])
        # displayStr = f"{displayStr}{str(thingsToBeAdded)} = {str(sum(thingsToBeAdded))}"
        df = pd.DataFrame(rollResults)
        total = sum(rollResults['Total'])
        if total < 0:
            totalStr = f"**NEGATIVE** {fuckWithPeople.replaceCharactersWithEmojis(total*-1)}"
        else:
            totalStr = fuckWithPeople.replaceCharactersWithEmojis(str(total))
        return f"The result of your roll is:\n```{df.to_string(index=False)}```\nWhich brings us to a grand total of {totalStr}!!!"

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

        # dictKeys = arg.split("+")
        # thingsToAdd = dict()
        # for key in dictKeys:
        #     thingsToAdd[key] = []
        #     regex = re.match(r"^([0-9]*)?(d([0-9]*))?$",key.lower())
        #     rollResults = []
        #     justANumber = False
        #     displayedResult = ""
        #     #TODO: Add handling for bad input
        #     if regex is not None and not regex[0] == "":
        #         if regex[1] == "":
        #             numOfDice = 1
        #         else:
        #             numOfDice = int(regex[1])
        #         if regex[2] == "":
        #             justANumber = True
        #         else:
        #             typeOfDice = int(regex[3])
        #         i=1
        #         if not justANumber:
        #             while i <= numOfDice: 
        #                 random.seed()
        #                 rollResults.append(random.randint(1,typeOfDice))
        #                 i += 1
        #         else:
        #             rollResults.append(numOfDice)
        #         thingsToAdd[key]= rollResults
        # for key in thingsToAdd.keys():
        #     displayedResult = f"{displayedResult}{key}={thingsToAdd[key]}={sum(thingsToAdd[key])}\n"
        # print(displayedResult)
        # pass


def setup(bot):
    bot.add_cog(diceRollingCog(bot))