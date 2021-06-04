from discord.enums import ActivityType
from discord.ext import commands

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

        if not message.guild: #on direct message taken, direct message to owner
            owner = await self.bot.fetch_user(181439459894624256)
            if message.author != owner:
                await owner.send(str(message.author) + ": " + str(message.content))

        else:
            if 'ratjam' in message.content.lower(): # if ratJam exists in the message, add its emote as a reaction
                await message.add_reaction('<a:ratJAM:823610543520612364>')


    @commands.Cog.listener()
    async def on_member_update(self, before, after): # log nickname-status-activity-role changes

        owner = await self.bot.fetch_user(181439459894624256)
        logs_channel = await self.bot.fetch_channel(850160971187486780)

        if not before == owner:

            if not before.nick == after.nick:
                await logs_channel.send(f"\"{before}\"s nickname has changed, \"{before.nick}\" to \"{after.nick}\"")

            elif not before.status == after.status:
                await logs_channel.send(f"\"{before}\"s status has changed, \"{before.status}\" to \"{after.status}\"")

            elif not before.activity == after.activity:
                if before.activity.type == ActivityType.streaming and after.activity.type == ActivityType.streaming:
                    await logs_channel.send(f"\"{before}\"s activity has changed, \"{str(before.activity.type)[13:]} {before.activity.name} at {before.activity.url} {before.activity.details}\" to \"{str(after.activity.type)[13:]} {after.activity.name} at {after.activity.url} {after.activity.details}\"")
                elif before.activity.type == ActivityType.streaming:
                    await logs_channel.send(f"\"{before}\"s activity has changed, \"{str(before.activity.type)[13:]} {before.activity.name} at {before.activity.url} {before.activity.details}\" to \"{str(after.activity.type)[13:]} {after.activity.name} {after.activity.details}\"")
                elif after.activity.type == ActivityType.streaming:
                    await logs_channel.send(f"\"{before}\"s activity has changed, \"{str(before.activity.type)[13:]} {before.activity.name} {before.activity.details}\" to \"{str(after.activity.type)[13:]} {after.activity.name} at {after.activity.url} {after.activity.details}\"")
                else:
                    await logs_channel.send(f"\"{before}\"s activity has changed, \"{str(before.activity.type)[13:]} {before.activity.name} {before.activity.details}\" to \"{str(after.activity.type)[13:]} {after.activity.name} {after.activity.details}\"")
                
            elif not before.roles == after.roles:
                await logs_channel.send(f"\"{before}\"s roles has changed, \"{before.roles}\" to \"{after.roles}\"")


    @commands.Cog.listener()
    async def on_user_update(self, before, after): # log avatar-username-discriminator changes

        owner = await self.bot.fetch_user(181439459894624256)
        logs_channel = await self.bot.fetch_channel(850160971187486780)

        if not before == owner:

            if not before.avatar == after.avatar:
                await logs_channel.send(f"\"{before}\" changed avatar: \"{before.avatar_url}\" to \"{after.avatar_url}\"")

            elif not before.name == after.name:
                await logs_channel.send(f"\"{before}\"s username has changed: \"{before.name}\" to \"{after.name}\"")

            elif not before.discriminator == after.discriminator:
                await logs_channel.send(f"\"{before}\"s discriminator has changed: \"{before.discriminator}\" to \"{after.discriminator}\"")

def setup(bot):
    bot.add_cog(Events(bot))
