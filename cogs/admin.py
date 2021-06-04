import discord
from discord.ext import commands
import sys
import os

from discord.ext.commands.converter import UserConverter

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    brief_delete = "Deletes messages"
    description_delete = "Deletes the number of messages given with command. Maximum deletion in one command is 50."
    brief_presence = "Changes bot activity"
    description_presence = "Changes activity of the bot. Activities can be playing, streaming, watching and listening. Everything takes an extra argument to show what are they doing in that activity. Streaming takes one more argument that is a twitch link."
    brief_prefix = "Changes prefix"
    description_prefix = "Changes the bot's prefix. If no arguments given, the prefix will be changed to \"!\"."
    brief_exit = "Disconnects the bot"
    description_exit = "Kills the bot. Only the owner can use it. So, don't bother writing it."
    brief_restart = "Restarts the bot"
    description_restart = "Restarts the bot. Bot needs approximately 3 seconds to wake up again."
    brief_load = "Loads a cog"
    description_load = "Loads a cog. Commands in that cog can be used now."
    brief_unload = "Unloads a cog"
    description_unload = "Unloads a cog. Commands in that cog can not be used now."
    brief_reload = "Reloads a cog"
    description_reload = "Reloads a cog. The cog will be updated."
    brief_dm = "Directs messages the specified"
    description_dm = "Directs messages the specified user with the given message."


    async def is_owner(ctx): #Checks if the author is the owner
        return ctx.author.id == 181439459894624256

    @commands.command(brief = brief_delete, description = description_delete)
    @commands.check(is_owner)
    async def delete(self, ctx, number : int):
        try:
            if ctx.guild is not None:
                message_number = number
                if message_number > 0:
                    if message_number > 50:
                        message_number = 50
                    await ctx.channel.purge(limit=message_number + 1)

                    if message_number == 1:
                        await ctx.channel.send(f"Deleted 1 message", delete_after=3.0)
                    else:
                        await ctx.channel.send(f"Deleted {message_number} messages", delete_after=3.0)
            else:
                await ctx.message.author.send("This command does not work on direct message.", reference = ctx.message)
        except:
                await ctx.channel.send("Exception occured")

    @commands.command(brief = brief_presence, description = description_presence)
    @commands.check(is_owner)
    async def presence(self, ctx, presence : str , * , activity : str = None, link : str = None):
        try:

            if presence == "playing":
                await self.bot.change_presence(activity=discord.Game(name=activity))
                await ctx.channel.send(f"Changed rich presence to \"Playing {activity}\"")

            elif presence == "streaming":
                await self.bot.change_presence(activity=discord.Streaming(name=activity, url=link))
                await ctx.channel.send(f"Changed rich presence to \"Streaming {activity}at {link}\"")

            elif presence == "listening":
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
                await ctx.channel.send(f"Changed rich presence to \"Listening to {activity}\"")

            elif presence == "watching":
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=activity))
                await ctx.channel.send(f"Changed rich presence to \"Watching {activity}\"")
                        
            elif presence == "reset":
                await self.bot.change_presence()
                        
            else:
                await ctx.channel.send("Wrong Input")
        except:
            await ctx.channel.send("Exception occured")

    @commands.command(brief = brief_prefix, description = description_prefix) 
    async def prefix(self, ctx, *, new_prefix : str = "!"):
        try:

            self.bot.command_prefix = new_prefix

            with open('prefix.txt', "w") as file:
                    file.write(new_prefix)
            await ctx.channel.send(f"Changed prefix to \"{new_prefix}\"")

        except:
            await ctx.channel.send("Exception occured")

    @commands.command(brief = brief_exit, description = description_exit)
    @commands.check(is_owner)
    async def exit(self, ctx):
        await ctx.channel.send("Disconnecting...")
        await self.bot.close()

    @commands.command(brief = brief_restart, description = description_restart)
    @commands.check(is_owner)
    async def restart(self, ctx):
        await ctx.channel.send("Restarting... Wait for 3 seconds.") # to make sure bot is connected after restarting
        python = sys.executable
        os.execl(python, python, * sys.argv)

    @commands.command(brief = brief_load, description = description_load)
    @commands.check(is_owner)
    async def load(self, ctx, cog_name : str):
        try:
            self.bot.load_extension(f"cogs.{cog_name}")
            await ctx.channel.send(f"Cog \"{cog_name}\" has been loaded.")
        except:
            await ctx.channel.send("Exception occured")

    @commands.command(brief = brief_unload, description = description_unload)
    @commands.check(is_owner)
    async def unload(self, ctx, cog_name : str):
        try:
            self.bot.unload_extension(f"cogs.{cog_name}")
            await ctx.channel.send(f"Cog \"{cog_name}\" has been unloaded.")
        except:
            await ctx.channel.send("Exception occured")

    @commands.command(brief = brief_reload, description = description_reload)
    @commands.check(is_owner)
    async def reload(self, ctx, cog_name : str = "all"):
        try:
            if cog_name == "all":
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        self.bot.reload_extension(f"cogs.{filename[:-3]}")
                await ctx.channel.send("All cogs have been reloaded.")
            else:
                self.bot.reload_extension(f"cogs.{cog_name}")
                await ctx.channel.send(f"Cog \"{cog_name}\" has been reloaded.")
        except:
            await ctx.channel.send("Exception occured")

    @commands.command(brief = brief_dm, description = description_dm)
    @commands.check(is_owner)
    async def dm(self, ctx, recipient : UserConverter, *, message : str):
        try:
            await recipient.send(message)
            await ctx.message.author.send(f"Sent \"{recipient}\" the message \"{message}\"")
        except:
            await ctx.channel.send("Exception occured")

def setup(bot):
    bot.add_cog(Admin(bot))
