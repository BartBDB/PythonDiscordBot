import discord
import logging
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from apikey import *
import threading
import random
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

#Happens when the bot starts
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(StatusArray[random.randint(0, len(StatusArray)-1)]))
    print("Bot is ready to do useful shit!\n")

#Status change every x seconds    
    
#@tasks.loop(seconds=statuschangetimer)
#async def statuschangetimerfunction():
#    print('timer hit')
#    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(StatusArray[random.randint(0, len(StatusArray)-1)]))


#Test command
@client.command()
async def test(ctx):
    await ctx.send("Test")
    await ctx.send(ctx.message.guild.name)


@client.command()
async def say(ctx):
    if ctx.author.id == ID:
        msg = ctx.message.content
        msgtosend = msg.replace("&say ", "")
        await ctx.send(msgtosend)
        await ctx.message.delete()
    else:
        await ctx.send("This command is only usable by the bot owner, ZeverousNova")
1

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == (None):
        reason = "No reason given."
    await ctx.send(f'User {member} has been kicked. Reason: '+ reason)
    channel = client.get_channel(LogChannelID)
    await channel.send((f"User {member} has been kicked by {client.get_user(ctx.author.id)}. Reason: " + reason))
    await member.send((f"You have been kicked from {ctx.message.guild.name}. Reason: " + reason))
    await member.kick(reason=reason)
    await ctx.message.delete()
    
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the required permissions to kick people. Nice try.")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason == (None):
        reason = "No reason given." 
    await ctx.send(f'User {member} has been banned. Reason: '+ reason)
    channel = client.get_channel(LogChannelID)
    await channel.send((f"User {member} has been banned by {client.get_user(ctx.author.id)}. Reason: " + reason))
    await member.send((f"You have been banned from {ctx.message.guild.name}. Reason: " + reason))
    await member.ban(reason=reason)
    await ctx.message.delete()

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the required permissions to ban people. Nice try.")

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency*1000, 1)))

#to do
#peg -bullets idea, not mine
#tell my why --aint nothing but an heartache
#ping kick ban mute warn

client.run(BOTTOKEN, log_handler=handler)