from discord.ext import commands

class Extras(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    brief_echo = "Echoes the message"
    description_echo = "Echoes the sentence given after command."

    @commands.command(brief = brief_echo, description = description_echo) 
    async def echo(self, ctx, *, arg : str):
        try:
            await ctx.message.delete()
            await ctx.send(arg)
        except:
            await ctx.channel.send("Exception occured")

def setup(bot):
    bot.add_cog(Extras(bot))
