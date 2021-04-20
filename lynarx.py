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
messages = joined = 0

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

    global messages
    messages += 1
    allowed_channels = ["bottest"]

    if str(message.channel) in allowed_channels:

        if message.content.startswith('$hello'):
            await message.reply('Hello!', mention_author=True)

        elif message.content.startswith('$help'):
            embed = discord.Embed(title = "Commands", description = "Description of the commands")
            embed.add_field(name = "$help", value = "Shows this window")
            embed.add_field(name = "$hello", value = "Greets the user with a reply")
            embed.add_field(name = "$dice", value = "Returns random number between 1 and 6")
            embed.add_field(name = "$dm", value = "Direct messages you with a test message")
            embed.add_field(name = "$thumb", value = "Returns the emoji(👍,👎) you reacted with back")
            await message.channel.send(content=None, embed=embed)

        elif message.content.startswith('$dice'):
            await message.channel.send(randint(1,6), mention_author=True)

        elif message.content.startswith('$users'):
            await message.channel.send(f"Number of Members: {message.guild.member_count}")
            
        elif message.content.startswith('$dm'):
            await message.author.send("test dm") # sends direct message to author

        elif not message.guild: # on direct message taken
            await message.channel.send('not answering to dms')

        elif message.content.startswith('$thumb'): # send back the chosen reaction
            channel = message.channel
            msg = await channel.send('Send me 👍 reaction in 10 seconds')
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '👍'

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('👎 timeout')
            else:
                await channel.send('👍')
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