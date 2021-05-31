from asyncio.windows_events import NULL
import discord
import random
import time
import datetime
import os
import sys
import math

def read_token(): #reads discord bot token from the txt
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

def read_prefix(): #reads the prefix it saved before
    with open("prefix.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = discord.Client()

aram_in_progress = False #initialize global variables
bot_prefix = read_prefix()


@client.event
async def on_connect(): #when connected to server print a message
    print("Connected to discord")


@client.event
async def on_ready(): #when ready to operate print the status
    print(f'Logged in as {client.user.name} (ID: {client.user.id}) (Latency: {int(client.latency*1000)}ms)')
    print("Ready")
    print('------')


@client.event
async def on_message(message): #when a message comes

    if message.author == client.user: #if the message comes from this bot, do nothing
        return


    global aram_in_progress #define global variables
    global bot_prefix

   
    allowed_channels = ["genel", "bottest", "bot", "aram"]


    if str(message.channel) in allowed_channels or not message.guild: # only work in allowed_channels or in private message

        if '<a:ratJAM:823610543520612364>' in message.content: # if ratJam exists in the message, add its emote as a reaction
            await message.add_reaction('<a:ratJAM:823610543520612364>')


        if not message.guild: #on direct message taken, send an answer and log the message
            await message.author.send("I don't answer to private messages")
            with open("dms.txt", "a", encoding="utf-8") as f:
                f.write(f"Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')} {message.author} : {message.content}  \n")

        elif message.content.startswith(bot_prefix + "help"): # shows help menu
            bot_channel = client.get_channel(594596796890873871) # gets the id of "bot" channel
            aram_channel = client.get_channel(848731423645106217) # gets the id of "aram" channel
            embed = discord.Embed(title = "Commands", description = "Description of the commands")
            embed.add_field(name = bot_prefix + "delete", value = "Deletes messages")
            embed.add_field(name = bot_prefix + "dice", value = "Returns random number between 1 and 6")
            embed.add_field(name = bot_prefix + "aram", value = f'only works in {bot_channel.mention} and {aram_channel.mention}')
            embed.add_field(name = bot_prefix + "restart", value = "Restarts the bot")
            embed.add_field(name = bot_prefix + "exit", value = "Disconnects the bot")
            embed.add_field(name = bot_prefix + "prefix", value = f"Changes the prefix, current \"{bot_prefix}\"")
            embed.add_field(name = bot_prefix + "teamup", value = "Creates two teams with given players")
            await message.channel.send(content=None, embed=embed)

        elif message.content.startswith(bot_prefix + "prefix"): #changes the prefix of bot default "!"
            try:
                if(len(message.content.split()) == 1):
                    bot_prefix = "!"
                else:
                    bot_prefix = message.content.split()[1]

                with open('prefix.txt', "w") as file:
                        file.write(bot_prefix)
                await message.channel.send(f"Changed prefix to \"{bot_prefix}\"")

            except:
                await message.channel.send(f"Wrong input")

        elif message.content.startswith(bot_prefix + "teamup"): #Creates two teams with given players
            try:
                player_list = message.content.split()[1:]
                team1_number = math.floor(len(player_list)/2)
                random.shuffle(player_list)
                team1 = ""
                team2 = ""

                embed = discord.Embed(title = "Teams")

                for player in player_list[:team1_number]:
                    team1 = team1 + "\n" + str(player)


                for player in player_list[team1_number:]:
                    team2 = team2 + "\n" + str(player)

                embed.add_field(name = "Team1", value = f"{team1}")
                embed.add_field(name = "Team2", value = f"{team2}")

                await message.channel.send(content=None, embed=embed)

            except:
                await message.channel.send(f"Wrong input")



        elif message.content.startswith(bot_prefix + "delete"): #deletes messages, 50 max in 1 run
            if(message.author.id == 181439459894624256): #only Sacrier#2869 can delete messages
                message_number = int(message.content.split()[1])
                if message_number > 0:
                    if message_number > 50:
                        message_number = 50
                    try:
                        await message.channel.purge(limit=message_number + 1)
                        await message.channel.send(f"Deleted {message_number} messages")
                    except:
                        await message.channel.send(f"Write a proper integer Ex. {bot_prefix}delete 5 " + message.author.mention, mention_author=True)

                    
        elif message.content.startswith(bot_prefix + "restart"): #restarts the bot by creating new process
            await message.channel.send("Restarting... Wait for 3 seconds.") # to make sure bot is connected after restarting
            python = sys.executable
            os.execl(python, python, * sys.argv)


        elif message.content.startswith(bot_prefix + "exit"): # exits
            if(message.author.id == 181439459894624256): #only Sacrier#2869 can shut down the bot
                await message.channel.send("Disconnecting...")
                await client.close()
            else:
                await message.channel.send("You can't shut down me " + message.author.mention, mention_author=True)


        elif message.content.startswith(bot_prefix + "dice"): # dice 1to6
            await message.channel.send(random.randint(1,6)  + " " + message.author.mention, mention_author=True)


        elif message.content.startswith(bot_prefix + "aram"): # tries to call people for aram
            try:
                if(message.channel.name in {"aram", "bot", "bottest"}):

                    aram_role = message.guild.get_role(847982643702267935) #gets the id of "Aram" role so it can ping

                    if aram_in_progress:
                        return

                    aram_in_progress = True

                    player_accepted = 0
                    if(len(message.content.split()) == 1):
                        player_needed = 5
                    else:
                        player_needed = int(message.content.split()[1])

                    if player_needed in {5, 6, 8, 10}:
                    
                        accepted_list = []
                        declined_list = []
                        accepted_string = ""
                        declined_string = ""
                        team1_string = ""
                        team2_string = ""

                        call_msg = "Hazırlık bitti, oyuna girin"

                        msg = await message.channel.send(f"Aram gelen ✅, gelmeyen ❌ {player_needed} kişi gerekiyor {aram_role.mention}")
                        await msg.add_reaction('✅')
                        await msg.add_reaction('❌')

                        def check(reaction, user):
                            return (str(reaction.emoji) == '✅') or (str(reaction.emoji) == '❌')

                        while player_accepted < player_needed:

                            reaction, user = await client.wait_for('reaction_add', check=check)

                            if user != client.user:

                                if str(reaction.emoji) == '✅':

                                    if user not in accepted_list and user not in declined_list:

                                        player_accepted += 1
                                        accepted_list.append(user)
                                        await message.channel.send(f"{user.mention} ✅ {player_accepted}/{player_needed}")
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
                                                random.shuffle(accepted_list)

                                                for player in accepted_list[:player_needed/2]:
                                                    team1_string = team1_string + "\n" + str(player)
                                                    call_msg = call_msg + " " + player.mention

                                                for player in accepted_list[player_needed/2:]:
                                                    team2_string = team2_string + "\n" + str(player)
                                                    call_msg = call_msg + " " + player.mention

                                                embed.add_field(name = "Team1", value = f"{team1_string}")
                                                embed.add_field(name = "Team2", value = f"{team2_string}")

                                            message.channel.send(content=None, embed=embed)
                                            await message.channel.send(call_msg)
                                            aram_in_progress = False

                                elif str(reaction.emoji) == '❌':

                                    if user not in declined_list and user not in accepted_list:
                                        declined_list.append(user)
                                        await message.channel.send(f"{user.mention} ❌")
                    else:
                        aram_in_progress = False
                        await message.channel.send(f"Wrong input. \"{bot_prefix}aram NoOfPlayers\" , only 5-6-8-10 works as numbers. 5 is default.")
            except:
                aram_in_progress = False
                await message.channel.send(f"Wrong input. \"{bot_prefix}aram NoOfPlayers\" , only 5-6-8-10 works as numbers. 5 is default.")



@client.event 
async def on_member_update(before, after): # log nickname-role changes

    if not before.nick == after.nick:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')},  {before} changed nickname, Before: {before.nick}, After: {after.nick}\n")

    else:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')}, {before} changed roles, Before: {before.roles}, After: {after.roles}\n")


@client.event
async def on_user_update(before, after): # log user avatar changes

    if not before.avatar == after.avatar:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')},  {before} changed avatar, Before: {before.avatar}, After: {after.avatar}\n")
    
client.run(token)