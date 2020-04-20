import discord
from discord.ext import commands
import math
import random
import re
import pandas as pd
import fuckWithPeople
import loggingAndErrors
import os
import collections
import functools
import math



class diceRollStats():
    def __init__(self,numOfDice,typeOfDice,drop_highest,drop_lowest,rollStats):
        self.numOfDice = numOfDice
        self.typeOfDice = typeOfDice
        self.drop_highest = drop_highest
        self.drop_lowest = drop_lowest
        self.rollStats = rollStats

    @functools.lru_cache(maxsize=None)
    def binomial(self,n, k):
        return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

    @functools.lru_cache(maxsize=None)
    def outcomes(self,count, sides, drop_highest, drop_lowest):
        d = collections.Counter()
        if count == 0:
            d[0] = 1
        elif sides == 0:
            pass
        else:
            for count_showing_max in range(count + 1):  # 0..count
                d1 = self.outcomes(self,count - count_showing_max, sides - 1,
                            max(drop_highest - count_showing_max, 0),
                            drop_lowest)
                count_showing_max_not_dropped = max(
                    min(count_showing_max - drop_highest,
                        count - drop_highest - drop_lowest), 0)
                sum_showing_max = count_showing_max_not_dropped * sides
                multiplier = self.binomial(self,count, count_showing_max)
                for k, v in d1.items():
                    d[sum_showing_max + k] += multiplier * v
        return d

    @classmethod
    def get_outcomes(self,count, sides, drop_highest, drop_lowest):
        self.rollStats = self.outcomes(self,count, sides, drop_highest, drop_lowest)



# def produceRollStats(*args):
#     d = outcomes(*args)
#     denominator = sum(d.values()) / 100
#     for k, v in sorted(d.items()):
#         print(k, v / denominator)
def mostLikelyRoll(numOfDice,diceType,drop_highest,drop_lowest):
    if diceType > 100:
        return "Error"
    elif diceType > 20 and numOfDice > 15:
        return "Error"
    elif diceType > 12 and numOfDice > 50:
        return "Error"
    elif diceType > 10 and numOfDice > 75:
        return "Error"
    elif diceType > 8 and numOfDice > 100:
        return "Error"
    elif diceType > 6 and numOfDice > 150:
        return "Error"
    elif diceType > 4 and numOfDice > 200:
        return "Error"
    if not numOfDice == 1:
        diceRollStats.get_outcomes(numOfDice,diceType,drop_highest,drop_lowest)
        if (numOfDice % 2) == 0:
            return str(diceRollStats.rollStats.most_common(1)[0][0])
        else:
            retVal = diceRollStats.rollStats.most_common(2)
            return f"{retVal[0][0]} or {retVal[1][0]}"
    else:
        return "NA"

class diceRolling:

    @classmethod
    def roll(self, arg: str):
        inputs = arg.split("+")
        resultsDict = {
            "Input":[],
            "AVG Roll":[],
            "Rolls":[],
            "Total":[]
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
                    resultsDict["AVG Roll"].append(mostLikelyRoll(int(numOfDice),int(typeOfDice),0,0))
                    resultsDict["Rolls"].append(rollResults)
                    resultsDict["Total"].append(sum(rollResults))
                for modifier in modifiers:
                    resultsDict["AVG Roll"].append("NA")
                    resultsDict["Input"].append(modifier)
                    resultsDict["Rolls"].append([int(modifier)])
                    resultsDict["Total"].append(int(modifier))
            return resultsDict

    @classmethod
    def validateInput(self, splitList: list):
        for roll in splitList:
            match = re.match("^(-?[0-9]{1,5})?(d([0-9]+))?(-[0-9]+)?$",roll.lower())
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
            return "The input for this roll wasn't correct or you input too large of a roll. Please try again."

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