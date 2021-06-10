import discord
from discord.ext import commands
import sys
import os

from discord.ext.commands.converter import UserConverter

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def is_owner(ctx): #Checks if the author is the owner
        return ctx.author.id == 181439459894624256

    @commands.command()
    @commands.check(is_owner)
    async def delete(self, ctx, number : int): #Deletes the number of messages given with command. Maximum deletion in one command is 50.
        """Deletes messages"""
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

    @commands.command()
    @commands.check(is_owner)
    async def presence(self, ctx, presence : str , * , activity : str = None, link : str = None): #Changes activity of the bot. Activities can be playing, streaming, watching and listening. Everything takes an extra argument to show what are they doing in that activity. Streaming takes one more argument that is a twitch link.
        """Changes bot activity"""
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

    @commands.command() 
    async def prefix(self, ctx, *, new_prefix : str = "!"): # Changes the bot's prefix. If no arguments given, the prefix will be changed to "!"
        """Changes the bot prefix"""
        try:

            self.bot.command_prefix = new_prefix

            with open('prefix.txt', "w") as file:
                    file.write(new_prefix)
            await ctx.channel.send(f"Changed prefix to \"{new_prefix}\"")

        except:
            await ctx.channel.send("Exception occured")

    @commands.command()
    @commands.check(is_owner)
    async def exit(self, ctx):
        """Disconnects the bot"""
        await ctx.channel.send("Disconnecting...")
        await self.bot.close()

    @commands.command()
    @commands.check(is_owner)
    async def restart(self, ctx): #Restarts the bot. Bot needs approximately 3 seconds to wake up again
        """Restarts the bot"""
        await ctx.channel.send("Restarting... Wait for 3 seconds.") # to make sure bot is connected after restarting
        python = sys.executable
        os.execl(python, python, * sys.argv)

    @commands.command()
    @commands.check(is_owner)
    async def load(self, ctx, cog_name : str): #Loads a cog. Commands in that cog can be used now.
        """Loads a cog"""
        try:
            self.bot.load_extension(f"cogs.{cog_name}")
            await ctx.channel.send(f"Cog \"{cog_name}\" has been loaded.")
        except:
            await ctx.channel.send("Exception occured")

    @commands.command()
    @commands.check(is_owner)
    async def unload(self, ctx, cog_name : str): #Unloads a cog. Commands in that cog can not be used now.
        """Unloads a cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog_name}")
            await ctx.channel.send(f"Cog \"{cog_name}\" has been unloaded.")
        except:
            await ctx.channel.send("Exception occured")

    @commands.command()
    @commands.check(is_owner)
    async def reload(self, ctx, cog_name : str = "all"): #Reloads a cog if a single arg given, if arg is "all" or there is none then reload all
        """Reloads a cog or all cogs"""
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

    @commands.command()
    @commands.check(is_owner)
    async def dm(self, ctx, recipient : UserConverter, *, message : str):
        """Directs messages the specified user"""
        try:
            await recipient.send(message)
            await ctx.message.author.send(f"Sent \"{recipient}\" the message \"{message}\"")
        except:
            await ctx.channel.send("Exception occured")

def setup(bot):
    bot.add_cog(Admin(bot))
