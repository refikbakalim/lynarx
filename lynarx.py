import discord
from random import randint
import asyncio
import time
import datetime

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

    if message.author == client.user:
        return

    global messages, player, aram
   
    messages += 1
    allowed_channels = ["genel", "bottest"]
    
    if str(message.channel) in allowed_channels:

        if '<a:ratJAM:823610543520612364>' in message.content:
            await message.add_reaction('<a:ratJAM:823610543520612364>')

        if message.content.startswith('$hello'):
            await message.reply('Hello!', mention_author=True)

        elif message.content.startswith('$help'):
            embed = discord.Embed(title = "Commands", description = "Description of the commands")
            embed.add_field(name = "$help", value = "Shows this window")
            embed.add_field(name = "$hello", value = "Greets the user with a reply")
            embed.add_field(name = "$dice", value = "Returns random number between 1 and 6")
            embed.add_field(name = "$dm", value = "Direct messages you with a test message")
            embed.add_field(name = "$aram", value = "aram")
            await message.channel.send(content=None, embed=embed)

        elif message.content.startswith('$dice'):
            await message.channel.send(randint(1,6), mention_author=True)

        elif message.content.startswith('$selftest'):
            await message.channel.send('$selftest')
        elif message.content.startswith('$users'):
            await message.channel.send(f"Number of Members: {message.guild.member_count}")
            
        elif message.content.startswith('$dm'):
            await message.author.send("test dm") # sends direct message to author

        elif not message.guild: # on direct message taken
            await message.channel.send('not answering to dms')

        elif message.content.startswith('$aram'):
            if aram:
                return
            aram = 1
            channel = message.channel
            playerNumber = 0
            player_list = []
            nplayer_list = []
            emptyPlayer = ""
            emptynPlayer = ""
            call_msg = "5 kişi çıktı oyuna girin"
            msg = await channel.send('Aram gelen ✅ atsın, gelmeyen ❌')
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
                            await channel.send(f"{user.mention} arama geliyor <a:ratJAM:823610543520612364> {playerNumber}/5")
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
                            await channel.send(f"{user.mention} gelmiyor <:sie_deep:645740921790398484>")
                
    else:
        print(f"""User:{message.author} tried to do command {message.content} in channel {message.channel}""")

@client.event
async def on_member_join(member): # Welcome the new member in general channel
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"Welcome to the server {member.mention}")

@client.event 
async def on_member_update(before, after): # log nickname-role changes
    if not before.nick == after.nick:
        with open("logs.txt", "a") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')},  {before} changed nickname, Before: {before.nick}, After: {after.nick}\n")
    else:
        with open("logs.txt", "a") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')}, {before} changed roles, Before: {before.roles}, After: {after.roles}\n")

@client.event
async def on_user_update(before, after): # log user avatar changes
    if not before.avatar == after.avatar:
        with open("logs.txt", "a") as f:
            f.write(f"Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')},  {before} changed avatar, Before: {before.avatar}, After: {after.avatar}\n")
    
@client.event        
async def update_stats(): # log the stats of server every 30 minutes
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"""Time: {int(time.time())}, Date:{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')}, Messages: {messages}, Members Joined: {joined}\n""")
    
            messages = 0
            joined = 0

            await asyncio.sleep(1800)
        except Exception as e:
            print(e)
            await asyncio.sleep(1800)

client.loop.create_task(update_stats())
client.run(token)