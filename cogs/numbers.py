from discord.ext import commands
from random import randint

class Numbers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    brief_dice = "Throws a dice"
    description_dice = "Returns a number ranged 1 to 6."
    brief_random = "Gets a random number"
    description_random = "Returns a random number from the given range. If one arguments is given the range is (1,given)."

    @commands.command(brief = brief_dice, description = description_dice)
    async def dice(self,ctx):
        try:
            await ctx.channel.send(f"{randint(1,6)}", reference = ctx.message)
        except:
            await ctx.channel.send(f"Exception occured")


    @commands.command(brief = brief_random, description = description_random) 
    async def random(self, ctx, *args : int):
        try:
            if(len(args) > 1):
                await ctx.channel.send(f"{randint(args[0],args[1])}", reference = ctx.message)
            else:
                await ctx.channel.send(f"{randint(1,args[0])}", reference = ctx.message)
        except:
            await ctx.channel.send("Exception occured")

def setup(bot):
    bot.add_cog(Numbers(bot))
