from discord.ext import commands
from discord.ext.commands.converter import MemberConverter, UserConverter

class Extras(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    brief_echo = "Echoes the message"
    description_echo = "Echoes the sentence given after command."
    brief_avatar = "Returns the avatar"
    description_avatar = "Returns the avatar of the user specified after the command"

    @commands.command(brief = brief_echo, description = description_echo) 
    async def echo(self, ctx, *, message : str):
        try:
            if ctx.guild is not None:
                await ctx.message.delete()
                await ctx.channel.send(message)
            else:
                await ctx.message.author.send("This command does not work on direct message.", reference = ctx.message)
        except:
            await ctx.channel.send("Exception occured")

    @commands.command(brief = brief_avatar, description = description_avatar) 
    async def avatar(self, ctx, user : UserConverter):
        try:
            await ctx.send(user.avatar_url)
        except:
            await ctx.channel.send("Exception occured")

def setup(bot):
    bot.add_cog(Extras(bot))
