import discord
import logging
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from apikey import BOTTOKEN
import random
import os
import asyncio

#Intents
intents = discord.Intents.default()
intents.members = True

#Logging
client = commands.Bot(command_prefix= '&', intents=discord.Intents.all())
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#Now playing status
statuschangetimer = 10
StatusArray = ["with code", "with Fools hope and dreams", "with Scizor", "with a gun", "Arknights", "Bluestacks", "Lethal Company", "Fools DND campaign", "with Provence"]

#Status change every x seconds    
    
#@tasks.loop(seconds=statuschangetimer)
#async def statuschangetimerfunction():
#    print('timer hit')
#    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(StatusArray[random.randint(0, len(StatusArray)-1)]))

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(StatusArray[random.randint(0, len(StatusArray)-1)]))
    print("Bot is ready to do useful shit!\n")


initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3]) #looks funny, but removes the .py at the end


async def load_extensions():
    if __name__ == '__main__':
        for extension in initial_extensions:
            await client.load_extension(extension)

async def main():
    async with client:
        await load_extensions()
        await client.start(BOTTOKEN)

asyncio.run(main())

#to do
#peg -bullets idea, not mine
#tell my why --aint nothing but an heartache
#ping kick ban mute warn