from asyncio.windows_events import NULL
from discord.ext import commands
import os
import discord

def read_prefix(): #reads the prefix it saved before
    with open("prefix.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix=read_prefix(), intents=intents)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.environ['LYNARX_DC_API_TOKEN'])