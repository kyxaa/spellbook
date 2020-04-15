import discord
from discord.ext import commands
import random
owlbearToken = '<:owlbearToken:697266516709605447>'
characterEmojis = {
    "1":"1️⃣",
    "2":"2️⃣",
    "3":"3️⃣",
    "4":"4️⃣",
    "5":"5️⃣",
    "6":"6️⃣",
    "7":"7️⃣",
    "8":"8️⃣",
    "9":"9️⃣",
    "0":"0️⃣",
    "A":"<:A_:699127896911904770>",
    "B":"<:B_:699127897188728863>",
    "C":"<:C_:699127896882544671>",
    "D":"<:D_:699127897344049242>",
    "E":"<:E_:699132142407385114>",
    "F":"<:F_:699127897373540362>",
    "G":"<:G_:699127897260294174>",
    "H":"<:H_:699127897243385956>",
    "I":"<:I_:699127897293717614>",
    "J":"<:J_:699127897465684069>",
    "K":"<:K_:699127897251643392>",
    "L":"<:L_:699127897289654313>",
    "M":"<:M_:699127897033670657>",
    "N":"<:N_:699127897537118249>",
    "O":"<:O_:699127896996053073>",
    "P":"<:P_:699127897566216192>",
    "Q":"<:Q_:699127897054773259>",
    "R":"<:R_:699127897025282059>",
    "S":"<:S_:699127897268682792>",
    "T":"<:T_:699127897016762379>",
    "U":"<:U_:699127897063161937>",
    "V":"<:V_:699127897520341012>",
    "W":"<:W_:699127897327403018>",
    "X":"<:X_:699127897356632125>",
    "Y":"<:Y_:699127897000116256>",
    "Z":"<:Z_:699127897109037077>"
}

# alphaEmojis = {
# "A":"🇦",
# "B":"🇧",
# "C":"🇨",
# "D":"🇩",
# "E":"🇪",
# "F":"🇫",
# "G":"🇬",
# "H":"🇭",
# "I":"🇮",
# "J":"🇯",
# "K":"🇰",
# "L":"🇱",
# "M":"🇲",
# "N":"🇳",
# "O":"🇴",
# "P":"🇵",
# "Q":"🇶",
# "R":"🇷",
# "S":"🇸",
# "T":"🇹",
# "U":"🇺",
# "V":"🇻",
# "W":"🇼",
# "X":"🇽",
# "Y":"🇾",
# "Z":"🇿"
# }

def randomAnimatedEmoji(ctx, numberOfEmojis):
    animatedEmojis = []
    if numberOfEmojis > len(ctx.bot.emojis):
        numberOfEmojis = len(ctx.bot.emojis)
    for emoji in ctx.bot.emojis:
        if emoji.animated:
            animatedEmojis.append(emoji)
    animatedEmojis = random.sample(animatedEmojis,numberOfEmojis)
    return animatedEmojis



def replaceCharactersWithEmojis(input: str):
    retVal = ""
    for character in input:
        if character.upper() in characterEmojis.keys():
            retVal = f"{retVal}{characterEmojis[character.upper()]}"
        else:
            retVal = f"{retVal}{character}"
    return retVal

# def replaceAlphaWithEmojis(number: int):
#     retVal = ""
#     for character in str(number):
#         retVal = f"{retVal}{numberEmojis[character]}"
#     return retVal
            


class fuckWithPeople(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
        # await def on_raw_reaction_add(self,payload):
        #     if payload.emoji.id == 697266516709605447 and payload.user_id == 158058710760030219:
        #         message = await self.bot.fetch_message(payload.message_id)

    @commands.command()
    async def emojiMe(self,ctx,*,input):
        await ctx.send(replaceCharactersWithEmojis(input))
        await ctx.message.delete()
        # if not payload.user_id == self.bot.user.id:
        #     if payload.emoji.id == 697266516709605447 and payload.user_id == 158058710760030219:
        #         channel = await self.bot.fetch_channel(payload.channel_id)
        #         user = await self.bot.fetch_user(payload.user_id)
        #         message = await channel.fetch_message(payload.message_id)
        #         await message.remove_reaction(payload.emoji,user)
        #         ctx = await self.bot.get_context(message)
        #         await ctx.message.edit(content=replaceCharactersWithEmojis(ctx.message.content))
        #         # animatedEmojis = randomAnimatedEmoji(ctx,20)
        #         # for animatedEmoji in animatedEmojis:
        #         #     await message.add_reaction(animatedEmoji)

    @commands.command()
    async def whoDoWeHate(self,ctx):
        await ctx.send("Eric Richards...Fuck that guy.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if not payload.user_id == self.bot.user.id:
            if payload.emoji.id == 697266516709605447 and payload.user_id == 158058710760030219:
                channel = await self.bot.fetch_channel(payload.channel_id)
                user = await self.bot.fetch_user(payload.user_id)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji,user)
                ctx = await self.bot.get_context(message)
                animatedEmojis = randomAnimatedEmoji(ctx,20)
                for animatedEmoji in animatedEmojis:
                    await message.add_reaction(animatedEmoji)
            # elif payload.user_id == 158058710760030219:
            #     channel = await self.bot.fetch_channel(payload.channel_id)
            #     user = await self.bot.fetch_user(payload.user_id)
            #     message = await channel.fetch_message(payload.message_id)
            #     if [emoji.me for emoji in message.reactions]:
            #         await message.clear_reactions()
                    


    
    # @commands.command()
    # async def clearYourReactions(self,ctx):
    #     if ctx.author.id == 158058710760030219:
    #         clearingReactions = False
    #         async for message in ctx.channel.history(limit=10):
    #             for reaction in message.reactions:
    #                 if reaction.me:
    #                     clearingReactions = True
    #                     break
    #             if clearingReactions:
    #                 break
    #         if clearingReactions:
    #             await ctx.send("Fine! I'll remove them.")
    #             await message.clear_reactions()



def setup(bot):
    bot.add_cog(fuckWithPeople(bot))