from discord.ext import commands

class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    brief_join = "Bot joins to voice channel"
    description_join = "Bot joins to the voice channel that its ID given as argument."

    @commands.command(brief = brief_join, description = description_join)
    async def join(self, ctx, arg : int):
        try:
            voice_channel = self.bot.get_channel(arg)
            await ctx.guild.change_voice_state(channel = voice_channel, self_mute=False, self_deaf=True)
            await ctx.channel.send(f"Lynarx joined to \"{voice_channel}\"")

        except:
            await ctx.channel.send(f"Exception occured")

def setup(bot):
    bot.add_cog(Voice(bot))
