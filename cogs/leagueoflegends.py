import discord
from discord.ext import commands
from random import shuffle
from math import floor

aram_in_progress = False #initialize global variables

class LeagueOfLegends(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    brief_teamup = "Makes teams"
    description_teamup = "Makes two team from the given list of names."
    brief_aram = "Arams the aram"
    description_aram ="Starts an invition for aram and builds teams when enough people accepts. Default is 5 players but if two teams needed 6, 8, 10 can be used."

    
    @commands.command(brief = brief_teamup, description = description_teamup)
    async def teamup(self, ctx, *args : str):
        try:
            player_list = list(args[:])
            team1_number = floor(len(player_list)/2)
            shuffle(player_list)
            team1 = ""
            team2 = ""

            embed = discord.Embed(title = "Teams")

            for player in player_list[:team1_number]:
                team1 = team1 + "\n" + str(player)


            for player in player_list[team1_number:]:
                team2 = team2 + "\n" + str(player)

            embed.add_field(name = "Team1", value = f"{team1}")
            embed.add_field(name = "Team2", value = f"{team2}")

            await ctx.channel.send(content=None, embed=embed, reference = ctx.message)

        except:
            await ctx.channel.send(f"Exception occured")

    @commands.command(brief = brief_aram, description = description_aram)
    async def aram(self, ctx, number : int = 5):
        try:
            if ctx.guild is not None:
                
                global aram_in_progress #define global variables

                aram_role = ctx.guild.get_role(847982643702267935) #gets the id of "Aram" role so it can ping
                owner = await self.bot.fetch_user(181439459894624256)

                if aram_in_progress:
                    return

                aram_in_progress = True
                message_list = []
                player_accepted = 0
                player_needed = number

                if player_needed in {5, 6, 8, 10}:
                        
                    accepted_list = []
                    declined_list = []
                    accepted_string = ""
                    declined_string = ""
                    team1_string = ""
                    team2_string = ""

                    call_msg = "Hazırlık bitti, oyuna girin"
                    uncall_msg = "Kişi sayısına ulaşılamadı"

                    original_msg = await ctx.channel.send(f"Aram gelen ✅, gelmeyen ❌ {player_needed} kişi gerekiyor {aram_role.mention}")
                    message_list.append(original_msg)
                    await original_msg.add_reaction('✅')
                    await original_msg.add_reaction('❌')
                    await original_msg.add_reaction('🇫')

                    def check(reaction, user):
                        if reaction.message.id == original_msg.id:
                            return (str(reaction.emoji) == '✅') or (str(reaction.emoji) == '❌') or (str(reaction.emoji) == '🇫')
                        else:
                            return False


                    while player_accepted < player_needed and aram_in_progress:

                        reaction, user = await self.bot.wait_for('reaction_add', check=check)

                        if user != self.bot.user:

                            if str(reaction.emoji) == '✅':

                                if user not in accepted_list and user not in declined_list:

                                    player_accepted += 1
                                    accepted_list.append(user)
                                    msg = await ctx.channel.send(f"{user.mention} ✅ {player_accepted}/{player_needed}")
                                    message_list.append(msg)
                                    if player_accepted == player_needed:

                                        if player_needed == 5:

                                            embed = discord.Embed(title = "Default Aram")

                                            for player in accepted_list:
                                                accepted_string = accepted_string + "\n" + str(player)
                                                call_msg = call_msg + " " + player.mention

                                            for nplayer in declined_list:
                                                declined_string = declined_string + "\n" + str(nplayer)

                                            embed.add_field(name = "Gelenler", value = f"{accepted_string}")
                                            embed.add_field(name = "Gelmeyenler", value = f"-{declined_string}")

                                        else:
                                            embed = discord.Embed(title = f"{player_needed/2}v{player_needed/2} Aram")
                                            shuffle(accepted_list)

                                            for player in accepted_list[:player_needed/2]:
                                                team1_string = team1_string + "\n" + str(player)
                                                call_msg = call_msg + " " + player.mention

                                            for player in accepted_list[player_needed/2:]:
                                                team2_string = team2_string + "\n" + str(player)
                                                call_msg = call_msg + " " + player.mention

                                            embed.add_field(name = "Team1", value = f"{team1_string}")
                                            embed.add_field(name = "Team2", value = f"{team2_string}")

                                        await ctx.channel.send(content=None, embed=embed)
                                        await ctx.channel.send(call_msg)
                                        for msg in message_list:
                                            await msg.delete()
                                        aram_in_progress = False

                            elif str(reaction.emoji) == '❌':

                                if user not in declined_list and user not in accepted_list:
                                    declined_list.append(user)
                                    msg = await ctx.channel.send(f"{user.mention} ❌")
                                    message_list.append(msg)

                            elif str(reaction.emoji) == '🇫':
                                if user.id == owner.id or user.id == ctx.author.id:
                                    for player in accepted_list:
                                            accepted_string = accepted_string + "\n" + str(player)
                                            uncall_msg = uncall_msg + " " + player.mention
                                    for msg in message_list:
                                            await msg.delete()
                                    await ctx.channel.send(uncall_msg)
                                    aram_in_progress = False
                else:
                    aram_in_progress = False
                    await ctx.channel.send("Wrong input.")

            else:
                await ctx.message.author.send("This command does not work on direct message.", reference = ctx.message)
        except:
            aram_in_progress = False
            await ctx.channel.send("Exception occured")

def setup(bot):
    bot.add_cog(LeagueOfLegends(bot))
