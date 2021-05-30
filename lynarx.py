import discord
from random import randint
import asyncio
import time
import datetime
import os
import sys

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
client = discord.Client()
messages = joined = player = aram = 0

@client.event
async def on_connect():
    print("Connected to discord")

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} (ID: {client.user.id}) (Latency: {int(client.latency*1000)}ms)')
    print("Ready")
    print('------')

@client.event
async def on_message(message):

    if message.author == client.user: #if the message comes from this bot, do nothing
        return

    global messages, player, aram
   
    messages += 1
    allowed_channels = ["genel", "bottest", "bot"]

    if str(message.channel) in allowed_channels or not message.guild: # only work in allowed_channels or in private message

        if '<a:ratJAM:823610543520612364>' in message.content: # if ratJam exists in a message, add as a reaction
            await message.add_reaction('<a:ratJAM:823610543520612364>')

        if not message.guild: # on direct message taken, log it
            await message.author.send("I don't answer to private messages")
            with open("dms.txt", "a", encoding="utf-8") as f:
                f.write(f"Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')} {message.author} : {message.content}  \n")

        elif message.content.startswith('$delete'): # deletes messages, 50 max in 1 run
            if(message.author.id == 181439459894624256):
                number = int(message.content.split()[1])
                if number > 50:
                    number = 50
                try:
                    await message.channel.purge(limit=number+1)
                except:
                    await message.channel.send("Write a proper integer Ex. $delete 5 " + message.author.mention, mention_author=True)
                    
        elif message.content.startswith('$restart'): #restarts the bot by creating new process
            await message.channel.send("Restarting... Wait for 3 seconds.")
            python = sys.executable
            os.execl(python, python, * sys.argv)

        elif message.content.startswith('$exit'): # exits
            if(message.author.id == 181439459894624256):
                await message.channel.send("Disconnecting...")
                await client.close()
            else:
                await message.channel.send("You can't close me " + message.author.mention, mention_author=True)

        elif message.content.startswith('$help'): # shows help menu
            text_channel = client.get_channel(594596796890873871)
            embed = discord.Embed(title = "Commands", description = "Description of the commands")
            embed.add_field(name = "$dice", value = "Returns random number between 1 and 6")
            embed.add_field(name = "$aram", value = f'only works in {text_channel.mention}')
            embed.add_field(name = "$restart", value = "Restarts the bot so $aram works again")
            embed.add_field(name = "$exit", value = "Disconnects the bot")
            await message.channel.send(content=None, embed=embed)

        elif message.content.startswith('$dice'): # dice 1to6
            await message.channel.send(randint(1,6), mention_author=True)

        elif message.content.startswith('$aram'): # tries to call people for aram
            if(message.channel.name == "bot"):
                aram_role = message.guild.get_role(847982643702267935)
                if aram:
                    return
                aram = 1
                channel = message.channel
                playerNumber = 0
                player_list = []
                nplayer_list = []
                emptyPlayer = ""
                emptynPlayer = ""
                call_msg = "Takım kuruldu oyuna girin"
                msg = await channel.send(f"Aram gelen ✅, gelmeyen ❌ {aram_role.mention}")
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')

                def check(reaction, user):
                    return (str(reaction.emoji) == '✅') or (str(reaction.emoji) == '❌')

                while playerNumber < 5:
                    reaction, user = await client.wait_for('reaction_add', check=check)
                    if user != client.user:
                        if str(reaction.emoji) == '✅':
                            if user not in player_list and user not in nplayer_list:
                                playerNumber += 1
                                player_list.append(user)
                                await channel.send(f"{user.mention} ✅ {playerNumber}/5")
                                if playerNumber == 5:
                                    embed = discord.Embed(title = "Aram")
                                    for player in player_list:
                                        emptyPlayer = emptyPlayer + "\n" + str(player)
                                        call_msg = call_msg + " " + player.mention
                                    for nplayer in nplayer_list:
                                        emptynPlayer = emptynPlayer + "\n" + str(nplayer)
                                    embed.add_field(name = "Gelenler", value = f"{emptyPlayer}")
                                    embed.add_field(name = "Gelmeyenler", value = f"-{emptynPlayer}")
                                    await message.channel.send(content=None, embed=embed)
                                    await channel.send(call_msg)
                                    aram = 0
                        elif str(reaction.emoji) == '❌':
                            if user not in nplayer_list and user not in player_list:
                                nplayer_list.append(user)
                                await channel.send(f"{user.mention} ❌")



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