# import requests
import discord
import os
from dotenv import load_dotenv
import pandas as pd
from discord.ext import commands
# ,owner_id='658080668886237194'
from config import invocation
bot = commands.Bot(command_prefix=invocation)
repoLink = "https://github.com/kyxaa/spellbook/"
import voiceAudio
import voiceMoveMembers
import fuckWithPeople
import dndSpells
import diceRolling
import guildSpecific
# import helpModule

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

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

    gitStatus = discord.Game(repoLink)
    await bot.change_presence(activity=gitStatus)

@bot.command()
async def readme(ctx):
    await ctx.send(f"The README for this bot can be found here: {repoLink}")

diceRolling.setup(bot)
voiceAudio.setup(bot)
voiceMoveMembers.setup(bot)
fuckWithPeople.setup(bot)
dndSpells.setup(bot)
guildSpecific.setup(bot)
bot.run(discord_token)