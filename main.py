import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
from nextcord.ext import application_checks
from apikey import *
import datetime
import logging
import random
import os
import time


#Intents
intents = nextcord.Intents.all()
intents.members = True

#Logging
client = commands.Bot(command_prefix= '&', intents=nextcord.Intents.all())

#Now playing status
statuschangetimer = 10

#Status change every x seconds    
    
#@tasks.loop(seconds=statuschangetimer)
#async def statuschangetimerfunction():
#    print('timer hit')
#    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(StatusArray[random.randint(0, len(StatusArray)-1)]))

#test command
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def test(interaction: nextcord.Interaction):
    """A simple command for testing purposes. Obviously."""
    await interaction.response.send_message("Test")
    await Interaction.response.send_message(self.message.guild.name)

#ping command
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def ping(interaction: nextcord.Interaction):
    """Pings Closure and sends her response time back in ms."""
    await interaction.response.send_message('Pong! {0}'.format(round(client.latency*1000, 1)))

#kick command and error
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
@application_checks.has_permissions(kick_members=True)
async def kick(interaction: nextcord.Interaction, member: nextcord.Member, reason=None):
    """Makes Closure kick a member out of the server."""
    if reason == (None):
        reason = "No reason given."
    await interaction.response.send_message(f'User **{member}** has been **kicked**. Reason: '+ reason)
    channel = client.get_channel(LogChannelID)
    await channel.send((f"User **{member}** has been **kicked** by **{interaction.user.global_name}**. Reason: " + reason))
    await member.send((f"You have been **kicked** from **{interaction.guild.name}**. Reason: " + reason))
    time.sleep(1/4) #not doing this results in the message not being sent and the bot erroring out.
    await member.kick(reason=reason)

@kick.error
async def kick_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message("You do not have the required permissions to kick people. Go bother Fool or someone about it instead.")
    else:
        raise error

#ban command and error
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
@application_checks.has_permissions(ban_members=True)
async def ban(interaction: nextcord.Interaction, member: nextcord.Member, reason=None):
    """Makes Closure ban a member out of the server."""
    if reason == (None):
        reason = "No reason given." 
    await interaction.response.send_message(f'User **{member}** has been **banned**. Reason: '+ reason)
    channel = client.get_channel(LogChannelID)
    await channel.send((f"User **{member}** has been **banned** by **{interaction.user.global_name}**. Reason: " + reason))
    await member.send((f"You have been **banned** from **{interaction.guild.name}**. Reason: " + reason))
    time.sleep(1/4) #not doing this results in the message not being sent and the bot erroring out.
    await member.ban(reason=reason)

@ban.error
async def ban_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message("You do not have the required permissions to ban people. Go bother Fool or someone about it instead.")
    else:
        raise error

#mute command
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
@application_checks.has_permissions(manage_roles=True)
async def mute(interaction: nextcord.Interaction, member: nextcord.Member, reason=None):
    """Makes Closure mute a member in the server."""
    if reason == (None):
        reason = "No reason given." 
    else: 
        await interaction.response.send_message(f'User **{member}** has been **muted**. Reason: '+ reason)
        channel = client.get_channel(LogChannelID)
        await channel.send((f"User **{member}** has been **muted** by **{interaction.user.global_name}**. Reason: " + reason))
        await member.send((f"You have been **muted** in **{interaction.guild.name}**. Reason: " + reason))
        await member.add_roles(interaction.guild.get_role(ZeroSMMutedRole))

@mute.error
async def mute_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message("You do not have the required permissions to mute people. Go bother Fool or someone about it instead.")
    else:
        raise error

#2 warnings, third one ban
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
@application_checks.has_permissions(manage_roles=True)
async def warn(interaction: nextcord.Interaction, member: nextcord.Member, reason=None):  
    """Makes Closure warn a member in the server."""
    channel = client.get_channel(LogChannelID)
    if reason == (None):
        reason = "No reason given." 
    if member.get_role(Strike2):
        await interaction.response.send_message(f'User **{member}** has been **warned a third time and got banned**. Reason: '+ reason)
        await channel.send((f"User **{member}** has been **warned a third time and got banned** by **{interaction.user.global_name}**. Reason: " + reason))
        await member.send((f"You have been **warned three times and got banned** from **{interaction.guild.name}**. Reason: " + reason))
        await member.ban(reason=reason)
    elif member.get_role(Strike1):
        await interaction.response.send_message(f'User **{member}** has been **warned a second time**. Reason: '+ reason)
        await channel.send((f"User **{member}** has been **warned a second time** by **{interaction.user.global_name}**. Reason: " + reason))
        await member.send((f"You have been **a second time** in **{interaction.guild.name}**. Reason: " + reason))
        await member.add_roles(interaction.guild.get_role(Strike2))
    else:  
        await interaction.response.send_message(f'User **{member}** has been **warned once**. Reason: '+ reason)
        await channel.send((f"User **{member}** has been **warned once** by **{interaction.user.global_name}**. Reason: " + reason))
        await member.send((f"You have been **warned once** in **{interaction.guild.name}**. Reason: " + reason))
        await member.add_roles(interaction.guild.get_role(Strike1))

@warn.error
async def warn_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message("You do not have the required permissions to warn people. Go bother Fool or someone about it instead.")
    else:
        raise error

#say command
@client.command()
async def say(ctx):
    if ctx.author.id == ID:
        msg = ctx.message.content
        msgtosend = msg.replace("&say ", "")
        await ctx.send(msgtosend)
        await ctx.message.delete()
    else:
        await ctx.message.delete()
        await ctx.send("This command is only usable by certain IDs.")


@client.event
async def on_message_delete(message):
    if (message.guild.id == ZeroSMServer):
        channel = client.get_channel(LogChannelID)
        if message.attachments:
            await channel.send((f"```Message deletion from {message.author}```Message: **{message.content}**\nIn: **{message.channel}**\nWith attachment: **{message.attachments}** "))
        else:
            await channel.send((f"```Message deletion from {message.author}```Message: **{message.content}**\nIn: **{message.channel}** "))
    
@client.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if (before.guild.id == ZeroSMServer):
        if (before.content != after.content):
            channel = client.get_channel(LogChannelID)
            if after.attachments or before.attachments:
                await channel.send((f"```New edit from {before.author}:```**Before: ** {before.content}\n**With attachment: **{before.attachments}\n**After: ** {after.content}\n**With attachment: ** {after.attachments}\n**In channel: **{after.channel}"))
            else:
                await channel.send((f"```New edit from {before.author}:```**Before: ** {before.content}\n**After: ** {after.content}\n**In channel: **{after.channel}"))


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send(ResponseArray[random.randint(0, len(ResponseArray)-1)])


@client.event
async def on_member_join(member):
    if (member.guild.id == ZeroSMServer):
        channel = client.get_channel(LogChannelID)
        await channel.send((f"```New member joined: {member.global_name}```Account created on **{member.created_at}**\n{member.display_avatar}"))

@client.event
async def on_member_remove(member):
    if (member.guild.id == ZeroSMServer):
        channel = client.get_channel(LogChannelID)
        await channel.send((f"```Member left: {member.global_name}```{member.display_avatar}"))





@tasks.loop(seconds=300)
async def updatestatus():
    await client.change_presence(status=nextcord.Status.dnd, activity=nextcord.Game(StatusArray[random.randint(0, len(StatusArray)-1)]))

@client.event
async def on_ready():
    print("Bot is ready to do useful shit!\n")
    updatestatus.start()

client.run(BOTTOKEN)


#to do
#peg -bullets idea, not mine
#tell my why --aint nothing but an heartache
#ping kick ban mute warn

#amongus sussy plushy