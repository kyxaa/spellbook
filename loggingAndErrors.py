from datetime import datetime
import logging

logging.basicConfig(
    handlers=[logging.FileHandler('logs.log', 'a', 'utf-8')],
    # filename='logs.log',
    format='<%(asctime)s> %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def writeToLogs(ctx,responseList):
    responseText = ""
    if hasattr(ctx.channel, "name"):
        channelName = ctx.channel.name
    else:
        channelName = "Direct Message"
    if ctx.guild is not None:
        guildName = ctx.guild.name
    else:
        guildName = "Not Applicable"
    for response in responseList:
        responseText = responseText + response
    logInfo = f"Activity Detected\n\
    USERNAME: {ctx.author.name}\n\
    CHANNEL: {channelName}\n\
    SERVER: {guildName}\n\
    REQUEST: {ctx.message.content}\n"
    print(f"<{datetime.now()}>: {logInfo}RESPONSE:\n{responseText[:100]}")
    logging.info(f"{logInfo}RESPONSE:\n{responseText}")