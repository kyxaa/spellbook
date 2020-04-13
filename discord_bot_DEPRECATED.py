import discord
import os
from dotenv import load_dotenv
import pandas as pd
import asyncio
import re
import spells
# import weather_api
# import reddit_bot.reddit_bot as reddit_bot
# from reddit_bot.reddit_bot import SearchData
from config import invocation
import logging
from datetime import datetime
import random
# logging.basicConfig(filename='logs.log',level=logging.INFO)
logging.basicConfig(
    filename='logs.log',
    format='<%(asctime)s> %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# def _url(path):
#     return "https://discordapp.com/api/v6/" + path



# CLASSES

# class GameInstance:
#     def __init__(self, player, game, game_information):
#         self.player = player
#         self.game = game
#         self.game_information = game_information


# class ApiConversation:
#     def __init__(self, id=None, user="", api="", expected_response="", message_to_api="", message_from_api="", last_exception="",other_data=None):
#         self.user = user
#         self.id = id
#         self.api = api
#         self.expected_repsonse = expected_response
#         self.message_to_api = message_to_api
#         self.message_from_api = message_from_api
#         self.last_exception = last_exception
#         self.other_data = other_data

# class RedditConversation(ApiConversation):
#     def __init__(self, id=None, user="", api="", expected_response="", message_to_api="", message_from_api="", last_exception="",other_data=None):
#         self.api= "reddit_bot"

#     async def send_message(self, message):
#         self.message_to_api = message.content
#         channel = message.channel
#         if self.expected_repsonse == "subreddit":
#             self.other_data = dict()
#             self.other_data["subreddit"] = message.content.strip()
#             if " " in self.other_data["subreddit"]:
#                 self.other_data["subreddit"] = self.other_data["subreddit"].split(" ")
#             self.message_from_api = "**What would you like to search?**\n`contain search in quotes(\") and if more than one seperate with commas(,)`"
#             await channel.send(self.message_from_api)
#             self.expected_repsonse = "search"
#         elif self.expected_repsonse == "search":
#             self.other_data["search"] = message.content.split(",")
#             self.other_data["search"] = [item.strip('\"') for item in self.other_data["search"]]
#             if len(self.other_data["search"]) == 1:
#                 self.other_data["search"] = self.other_data["search"][0]
#             self.message_from_api = "*Would you like an exact search?**\n`Yes = Exact Search, No = Search within the comments`"
#             await channel.send(self.message_from_api)
#             self.expected_repsonse = "exact_search"
#         elif self.expected_repsonse == "exact_search":
#             search_data = SearchData(self.other_data["subreddit"], self.other_data["search"], string_to_bool(message.content))
#             await channel.send("Let me look that up for you, this may take a minute.")
#             try:
#                 reddit_bot.search_subreddit_comments(search_data, limit_number=10)
#                 output = ""
#                 for i, url in enumerate(search_data.get_comment_urls()):
#                     result_number = i + 1
#                     if not output:
#                         output = f"<@{message.author.id}>, your results are ready!\nResult {result_number}: {url}\n"
#                     elif output:
#                         output = output + f"Result {result_number}: {url}\n"
#                 if len(output) and len(output) < 2000:
#                     await channel.send(output)
#                 elif len(output) >= 2000:
#                     multi_output = split_long_output_on_newline(output)
#                     for output in multi_output:
#                         await channel.send(output)
#                 else:
#                     await channel.send(f"<@{message.author.id}>, there were no comments found.")
#             except Exception as e:
#                 await channel.send("You made the reddit bot unhappy...check your command and try again.")
#                 print(f"Error from Reddit Bot: {e}")
#             current_conversations.remove(self)
#             del self



# class WeatherConversation(ApiConversation):
#     def __init__(self, id=None, user="", api="", expected_response="", message_to_api="", message_from_api="", last_exception="",other_data=None):
#         self.api= "weather_api"

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
client = discord.Client()

# current_conversations = []
# user = message.author
# other_bot = "reddit_bot"
# listen_for_response = True


# FUNCTIONS

def split_long_output_on_newline(output):
    split_outputs = output.splitlines()
    seperator = "\n"
    new_outputs = []
    while len(split_outputs) >= 16:
        new_outputs.append(seperator.join(split_outputs[:15]))
        split_outputs = split_outputs[15:]
    new_outputs.append(seperator.join(split_outputs))
    return new_outputs

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
        if numberofCharacters > 1900:
            listItem = '\n'.join(tempList[beginString:i]) + "\n"
            retVal.append(listItem)
            beginString = i + 1
            numberofCharacters = 0
        if string == tempList[-1]:
            retVal.append('\n'.join(tempList[beginString:]))
        i += 1
    return retVal

def string_to_bool(input):
  return input.lower() in ("yes", "true", "t", "1", "y")

def fetch_member_list(level_of_detail, guild):
    if level_of_detail == "names":
        name_list = '\n - '.join(member.name for member in guild.members)
        return str(f"Guild Members:\n - {name_list}")
    elif level_of_detail == "detailed":
        member_list = {
            "Name":[],
            "Status":[],
            "Activity":[],
            "ID":[]
        }
        for member in guild.members:
            member_list["Name"].append(member.name)
            member_list["Status"].append(str(member.status))
            if not member.activities:
                member_list["Activity"].append('')
            else:
                member_list["Activity"].append(member.activity.name)
            member_list["ID"].append(member.id)

        df = pd.DataFrame(member_list)
        return df.to_string(index=False)

async def console_display_users(guild):
    while True:
        print(fetch_member_list("detailed", guild))
        await asyncio.sleep(10)

# EVENTS

@client.event
async def on_ready():
    # channel = discord.utils.get(guild.text_channels, name='testing')
    # print(
    #     f"{client.user} has connected to the Discord guild {guild}!\n"
    #     f"{guild}'s id is {guild.id}"
    # )
    # await channel.send("The answer was right there in front of you...you should have made sure you were passing in a string into the re methods.")
    print("Connecting to:")
    for guild in client.guilds:
        print(guild.name)
    # creativename = discord.utils.get(guild.members, name="creativename")
    # print(creativename.is_on_mobile())
    # await creativename.create_dm()
    # await creativename.dm_channel.send("hi")
    # jawshie = discord.utils.get(guild.members, name="jawshie")
    # await jawshie.create_dm()
    # await jawshie.dm_channel.send("hi")

@client.event
async def on_message(message):
    # guild = message.guild
    channel = message.channel
    responseList = []
    # if message.channel.type.name == "private":
    #     isDM = True
    #     channel = message.channel
    # else:
    #     isDM = False
    #     channel = discord.utils.get(guild.text_channels, name=str(message.channel))
    # message_sent = False

    # if len(current_conversations) > 0:
    #     for conversation in current_conversations:
    #         if conversation.user == message.author:
    #             if isinstance(conversation, RedditConversation):
    #                 await conversation.send_message(message)

    # else:
    #     if message.content == f"{invocation} help":
    #         with open("discord_bot_help.txt") as file:
    #             help = file.read()
    #             await channel.send(help)

        # DISPLAY MEMBERS
    # if message.content == f"{invocation} display members":
    #     member_list = fetch_member_list('detailed', guild)
    #     messageToSend
    #     if not isDM:
    #         await channel.send(f"I'd be more than happy to do that, {message.author.name}!\n\n`{member_list}`")
    #     else:
    #         await client.send_message(message.author, )
    # if message.content == f"{invocation} display members":
    #     member_list = fetch_member_list('detailed', guild)
    #     messageToSend
    #     if not isDM:
    #         await channel.send(f"I'd be more than happy to do that, {message.author.name}!\n\n`{member_list}`")
    #     else:
    #         await client.send_message(message.author, )
    if message.author.id == 695782503759478794:
        guild = discord.utils.get(client.guilds, name='D&D 3 oh god not the BEES')
        emojis = random.sample(guild.emojis,3)
        for emoji in emojis:
            await message.add_reaction(emoji)
        logging.info(f"tagged Killbot\n\
    REQUEST: {message.content}\n")


    if message.content.lower().startswith("!spell "):
        if message.author.id == 695782503759478794:
            messageForKillBot = "Really? You think that will work?"
            await channel.send(messageForKillBot)
            responseList.append(messageForKillBot)
        else:
            spellName = re.sub(f"!spell[\s]*", "", message.content.lower())
            spellInfo = spells.displaySpell(spellName)
            if spellInfo is not None:
                if len(spellInfo) > 1999:
                    responseList = convertLongResponseToArray(spellInfo)
                else:
                    responseList.append(spellInfo)
                for response in responseList:
                    await channel.send(response)
            else:
                responseList.append("Make sure you spelled your spell name correctly. The format for that command is \n```!spell [name of spell]```")
                for response in responseList:
                    await channel.send(response)

    
    if message.content.lower().startswith("!spelllist "):
        if message.author.id == 695782503759478794:
            messageForKillBot = "Really, Killbot?? Do you think I'll be defeated that easily?????"
            await channel.send(messageForKillBot)
            responseList.append(messageForKillBot)
        else:
            spellClass = re.sub(f"!spelllist[\s]*", "", message.content.lower())
            spellList = spells.displaySpellList(spellClass)
            if spellList is not None:
                if len(spellList) > 1999:
                    responseList = convertLongResponseWithLinesToArray(spellList)
                else:
                    responseList.append(spellList)
                for response in responseList:
                    if response == responseList[0]:
                        await channel.send(f"__**{spellClass.title()} Spells**__\n```{response}```")
                    else:
                        await channel.send(f"```{response}```")
            else:
                responseList.append("Make sure you spelled the class name correctly. The format for that command is\n```!spelllist [class]```")
                for response in responseList:
                    await channel.send(response)

    if not responseList == []:
        responseText = ""
        if hasattr(channel, "name"):
            channelName = channel.name
        else:
            channelName = "Direct Message"
        if message.guild is not None:
            guildName = message.guild.name
        else:
            guildName = "Not Applicable"
        for response in responseList:
            responseText = responseText + response
        logging.info(f"Activity Detected\n\
    USERNAME: {message.author.name}\n\
    CHANNEL: {channelName}\n\
    SERVER: {guildName}\n\
    REQUEST: {message.content}\n\
    RESPONSE:\n{responseText}")

    # if message.content == f"{invocation} Gimble":
    #     await channel.send("<:gimbleToken:678100778996465671>")
    #     # ECHO
    #     if message.content.startswith(f"{invocation} echo "):
    #         echo = re.sub(f"{invocation} echo ", "", message.content)
    #         await channel.send(echo)

    #     if message.content == f"{invocation} lastecho":
    #         if echo:
    #             await channel.send(echo)
    #     # SLAPS
    #     if message.content.startswith(f"{invocation} slap "):
    #         slapee = re.sub(f"{invocation} slap ", "", message.content)
    #         slapping_list = []
    #         # slapees = str()
    #         if len(message.mentions) > 1:
    #             for member in message.mentions:
    #                 slapping_list.append(f"<@{member.id}>")
    #             str_slaps = ", ".join(slapping_list)
    #             await channel.send(f"That's alot of slapping! Imma slap {str_slaps}!!!")
    #         elif len(message.mentions) == 1:
    #             await channel.send(f"On behalf of the mighty {message.author.name}, Imma slap the living hell out of <@{message.mentions[0].id}>!!!")
    #         else:
    #             for member in guild.members:
    #                 if member.name == slapee:
    #                     await channel.send(f"On behalf of the mighty {message.author.name}, Imma slap the living hell out of <@{member.id}>!!!")
    #                     message_sent = True
    #             if not message_sent:
    #                 await channel.send(f"I'm confused as to who I should be slapping and will slap <@{message.author.id}>!!!")
    #     # BREAK
    #     if message.content.startswith('Can we take a break?'):
    #         await channel.send(f"I guess, you lazy sod.")
    #     # TESTING
    #     if message.content.startswith(f"{invocation} testing"):
    #         pass
    #         # for member in message.mentions:
    #         #     print(f"{member.name}"")
    #     # WEATHER
    #     if message.content.startswith(f"{invocation} weather "):
    #         weather_conversation = WeatherConversation()
    #         weather_conversation.mesage_to_api = re.sub(f"{invocation} weather ", "", message.content)
    #         try:
    #             weather_conversation.message_from_api = weather_api.weather_zip(weather_conversation.mesage_to_api)
    #             await channel.send(f"`{weather_conversation.message_from_api}`")
    #         except Exception as ex:
    #             # handle the error
    #             await channel.send(ex)
    #             weather_conversation.last_exception = ex
    #     # REDDIT SEARCH
    #     if message.content == f"{invocation} reddit comment search":
    #         reddit_conversation = RedditConversation()
    #         reddit_conversation.message_from_api = f"**Which subreddit(s) would you like to search within?**\n`if more than one sub, seperate by space`"
    #         reddit_conversation.user = message.author
    #         reddit_conversation.expected_repsonse = "subreddit"
    #         await channel.send(reddit_conversation.message_from_api)
    #         current_conversations.append(reddit_conversation)


            # search_params = search_params.split("] [")
            # search_params[0] = search_params[0][1 : : ]
            # search_params[-1] = search_params[-1][:-1:]
            # search_data = SearchData(search_params[0], search_params[1])
            # if len(search_params) > 2:
            #     if search_params[2].lower() == "within":
            #         search_data.exact_search = False
            # try:
            #     rb.search_subreddit_comments(search_data, limit_number=10)
            #     output = ""
            #     for i, url in enumerate(search_data.get_comment_urls()):
            #         result_number = i + 1
            #         if not output:
            #             output = f"Result {result_number}: {url}\n"
            #         elif output:
            #             output = output + f"Result {result_number}: {url}\n"
            #     if output:
            #         await channel.send(output)
            #     else:
            #         await channel.send("No comments found.")
            # except Exception as e:
            #     await channel.send("You made the reddit bot unhappy...check your command and try again.")
            #     print(f"Error from Reddit Bot: {e}")




# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f"Welcome to the sexiest place on Discord!!!"
#     )

# RUNNING CLIENT

client.run(discord_token)