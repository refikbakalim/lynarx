from asyncio.windows_events import NULL
import discord
from random import randint, shuffle
import time
import datetime
import os
import sys
from math import floor
from discord.ext import commands

def read_token(): #reads discord bot token from the txt
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

def read_prefix(): #reads the prefix it saved before
    with open("prefix.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
bot_prefix = read_prefix()

bot = commands.Bot(command_prefix=bot_prefix)

aram_in_progress = False #initialize global variables

@bot.event
async def on_connect(): #when connected to server print a message
    print("Connected to discord")


@bot.event
async def on_ready(): #when ready to operate print the status
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id}) (Latency: {int(bot.latency*1000)}ms)')
    print("Ready")
    print('------')


@bot.event
async def on_message(message): #when a message comes

    await bot.process_commands(message) #procces the commands first before looking into message

    if message.author == bot.user: #if the message comes from this bot, do nothing
        return

    if not message.guild: #on direct message taken, send an answer and log the message
        await message.author.send("I don't answer to private messages")
        with open("dms.txt", "a", encoding="utf-8") as f:
            f.write(f"Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')} {message.author} : {message.content}  \n")

    else:
        if 'ratjam' in message.content.lower(): # if ratJam exists in the message, add its emote as a reaction
            await message.add_reaction('<a:ratJAM:823610543520612364>')

    
            
@bot.command()
async def join(ctx, arg : int):
    try:
        voice_channel = bot.get_channel(arg)
        await ctx.guild.change_voice_state(channel = voice_channel, self_mute=False, self_deaf=True)
        await ctx.channel.send(f"Lynarx joined to \"{voice_channel}\"")

    except:
        await ctx.channel.send(f"Exception occured")

@bot.command()
async def delete(ctx, arg : int):
    try:
        if(ctx.author.id == 181439459894624256): #only Sacrier#2869 can delete messages
            message_number = arg
            if message_number > 0:
                if message_number > 50:
                    message_number = 50
                await ctx.channel.purge(limit=message_number + 1)

                if message_number == 1:
                    await ctx.channel.send(f"Deleted 1 message", delete_after=3.0)
                else:
                    await ctx.channel.send(f"Deleted {message_number} messages", delete_after=3.0)
    except:
            await ctx.channel.send(f"Exception occured")

@bot.command()
async def dice(ctx):
    try:
        await ctx.channel.send(f"{randint(1,6)} {ctx.author.mention}")
    except:
        await ctx.channel.send(f"Exception occured")

@bot.command()
async def presence(ctx, *args : str):
    try:
        if(ctx.author.id == 181439459894624256): #only Sacrier#2869 can change presence
            presence = args[0]
            activity = ""
            for elem in args[1:]:
                activity += elem + " "

            if presence == "playing":
                await bot.change_presence(activity=discord.Game(name=activity))
                await ctx.channel.send(f"Changed rich presence to \"Playing {activity}\"")

            elif presence == "streaming":
                length = len(args)
                activity = ""
                link = args[length-1]
                for elem in args[1:length-1]:
                    activity += elem + " "
                await bot.change_presence(activity=discord.Streaming(name=activity, url=link))
                await ctx.channel.send(f"Changed rich presence to \"Streaming {activity}at {link}\"")

            elif presence == "listening":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
                await ctx.channel.send(f"Changed rich presence to \"Listening to {activity}\"")

            elif presence == "watching":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=activity))
                await ctx.channel.send(f"Changed rich presence to \"Watching {activity}\"")
                    
            elif presence == "reset":
                await bot.change_presence()
                    
            else:
                await ctx.channel.send(f"Wrong Input")
    except:
        await ctx.channel.send(f"Exception occured")

@bot.command() 
async def random(ctx, *args : int):
    try:
        if(len(args) > 1):
            await ctx.channel.send(f"{randint(args[0],args[1])} {ctx.author.mention}")
        else:
            await ctx.channel.send(f"{randint(1,args[0])} {ctx.author.mention}")
    except:
        await ctx.channel.send("Exception occured")

@bot.command() 
async def echo(ctx, *args : str):
    try:
        await ctx.message.delete()
        await ctx.send(" ".join(args))
    except:
        await ctx.channel.send("Exception occured")

@bot.command() 
async def teamup(ctx, *args : str):
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

        await ctx.channel.send(content=None, embed=embed)

    except:
        await ctx.channel.send(f"Exception occured")

@bot.command() 
async def prefix(ctx, *args : str):
    try:
        global bot_prefix
        if(len(args) == 0):
            bot_prefix = "!"
        else:
            bot_prefix = " ".join(args)

        bot.command_prefix = bot_prefix

        with open('prefix.txt', "w") as file:
                file.write(bot_prefix)
        await ctx.channel.send(f"Changed prefix to \"{bot_prefix}\"")

    except:
        await ctx.channel.send(f"Wrong input")

@bot.command()
async def exit(ctx):
    if(ctx.author.id == 181439459894624256): #only Sacrier#2869 can shut down the bot
        await ctx.channel.send("Disconnecting...")
        await bot.close()
    else:
        await ctx.channel.send(f"You can't shut down me {ctx.author.mention}")

@bot.command()
async def restart(ctx):
    await ctx.channel.send("Restarting... Wait for 3 seconds.") # to make sure bot is connected after restarting
    python = sys.executable
    os.execl(python, python, * sys.argv)

@bot.command()
async def aram(ctx, *args : int):
    try:
        global aram_in_progress #define global variables
        if(ctx.channel.name in {"aram", "bot", "bottest"}):

            aram_role = ctx.guild.get_role(847982643702267935) #gets the id of "Aram" role so it can ping

            if aram_in_progress:
                return

            aram_in_progress = True

            player_accepted = 0
            if(len(args) == 0):
                player_needed = 5
            else:
                player_needed = args[0]

            if player_needed in {5, 6, 8, 10}:
                    
                accepted_list = []
                declined_list = []
                accepted_string = ""
                declined_string = ""
                team1_string = ""
                team2_string = ""

                call_msg = "Hazırlık bitti, oyuna girin"
                uncall_msg = "Aram iptal"

                msg = await ctx.channel.send(f"Aram gelen ✅, gelmeyen ❌ {player_needed} kişi gerekiyor {aram_role.mention}")
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                await msg.add_reaction('🇫')

                def check(reaction, user):
                    return (str(reaction.emoji) == '✅') or (str(reaction.emoji) == '❌') or (str(reaction.emoji) == '🇫')

                while player_accepted < player_needed and aram_in_progress:

                    reaction, user = await bot.wait_for('reaction_add', check=check)

                    if user != bot.user:

                        if str(reaction.emoji) == '✅':

                            if user not in accepted_list and user not in declined_list:

                                player_accepted += 1
                                accepted_list.append(user)
                                await ctx.channel.send(f"{user.mention} ✅ {player_accepted}/{player_needed}")
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

                                    ctx.channel.send(content=None, embed=embed)
                                    await ctx.channel.send(call_msg)
                                    aram_in_progress = False

                        elif str(reaction.emoji) == '❌':

                            if user not in declined_list and user not in accepted_list:
                                declined_list.append(user)
                                await ctx.channel.send(f"{user.mention} ❌")

                        elif str(reaction.emoji) == '🇫':
                            if user.id == 181439459894624256:
                                for player in accepted_list:
                                        accepted_string = accepted_string + "\n" + str(player)
                                        uncall_msg = uncall_msg + " " + player.mention
                                await ctx.channel.send(uncall_msg)
                                aram_in_progress = False
            else:
                aram_in_progress = False
                await ctx.channel.send(f"Wrong input. \"{bot_prefix}aram NoOfPlayers\" , only 5-6-8-10 works as numbers. 5 is default.")
    except:
        aram_in_progress = False
        await ctx.channel.send("Exception occured")


@bot.event 
async def on_member_update(before, after): # log nickname-role changes

    if not before.nick == after.nick:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')},  {before} changed nickname, Before: {before.nick}, After: {after.nick}\n")

    else:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')}, {before} changed roles, Before: {before.roles}, After: {after.roles}\n")


@bot.event
async def on_user_update(before, after): # log user avatar changes

    if not before.avatar == after.avatar:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')},  {before} changed avatar, Before: {before.avatar}, After: {after.avatar}\n")
    
bot.run(token)