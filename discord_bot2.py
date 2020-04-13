# import requests
import discord
import os
from dotenv import load_dotenv
import pandas as pd
from discord.ext import commands
# ,owner_id='658080668886237194'
from config import invocation
bot = commands.Bot(command_prefix=invocation)

import voiceAudio
import voiceMoveMembers
import fuckWithPeople
import dndSpells
import diceRolling

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

    gitStatus = discord.Game(name="https://github.com/kyxaa/spellbook/")
    await bot.change_presence(activity=gitStatus)


diceRolling.setup(bot)
voiceAudio.setup(bot)
voiceMoveMembers.setup(bot)
fuckWithPeople.setup(bot)
dndSpells.setup(bot)
bot.run(discord_token)