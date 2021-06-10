from discord.ext import commands
from discord.ext.commands.converter import MemberConverter, UserConverter

class Extras(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command() 
    async def echo(self, ctx, *, message : str):
        """Echoes the message"""
        try:
            logs_channel = await self.bot.fetch_channel(850160971187486780)
            if ctx.guild is not None:
                await ctx.message.delete()
                await ctx.channel.send(message)
                await logs_channel.send(f"\"{ctx.author}\" used echo, \"{ctx.message.content}\"")
            else:
                await ctx.message.author.send("This command does not work on direct message.", reference = ctx.message)
        except:
            await ctx.channel.send("Exception occured")

    @commands.command() 
    async def avatar(self, ctx, user : UserConverter = None): #Returns the avatar, if no user specified self avatar is returned
        """Returns the avatar"""
        try:
            logs_channel = await self.bot.fetch_channel(850160971187486780)
            if user == None:
                await ctx.send(ctx.author.avatar_url)
                await logs_channel.send(f"\"{ctx.author}\" used avatar, \"{ctx.message.content}\"")
            else:
                await ctx.send(user.avatar_url)
                await logs_channel.send(f"\"{ctx.author}\" used avatar, \"{ctx.message.content}\"")
        except:
            await ctx.channel.send("Exception occured")

def setup(bot):
    bot.add_cog(Extras(bot))
