from discord.ext import commands
import time
import datetime

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self): #when connected to server print a message
        print("Connected to discord")


    @commands.Cog.listener()
    async def on_ready(self): #when ready to operate print the status
        print(f'Logged in as {self.bot.user.name} (ID: {self.bot.user.id}) (Latency: {int(self.bot.latency*1000)}ms)')
        print("Ready")
        print('------')

    @commands.Cog.listener()
    async def on_message(self, message): #when a message comes

        if message.author == self.bot.user: #if the message comes from this bot, do nothing
            return

        if not message.guild: #on direct message taken, send an answer and log the message
            await message.author.send("I don't answer to private messages")
            with open("dms.txt", "a", encoding="utf-8") as f:
                f.write(f"Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')} {message.author} : {message.content}  \n")

        else:
            if 'ratjam' in message.content.lower(): # if ratJam exists in the message, add its emote as a reaction
                await message.add_reaction('<a:ratJAM:823610543520612364>')


    @commands.Cog.listener()
    async def on_member_update(self, before, after): # log nickname-role changes

        if not before.nick == after.nick:
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')},  \"{before}\" changed nickname, Before: \"{before.nick}\", After: \"{after.nick}\"\n")

        else:
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')}, \"{before}\" changed roles, Before: \"{before.roles}\", After: \"{after.roles}\"\n")


    @commands.Cog.listener()
    async def on_user_update(self, before, after): # log user avatar changes

        if not before.avatar == after.avatar:
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')},  {before} changed avatar, Before: {before.avatar}, After: {after.avatar}\n")

def setup(bot):
    bot.add_cog(Events(bot))
