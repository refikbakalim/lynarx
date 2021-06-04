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
    async def random(self, ctx, number1 : int, number2 : int = None):
        try:
            if number2 is not None:
                await ctx.channel.send(f"{randint(number1,number2)}", reference = ctx.message)
            else:
                await ctx.channel.send(f"{randint(1,number1)}", reference = ctx.message)
        except:
            await ctx.channel.send("Exception occured")

def setup(bot):
    bot.add_cog(Numbers(bot))
