import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
from nextcord.ext import application_checks
from apikey import *
import datetime
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

#test command
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def test(interaction: nextcord.Interaction):
    """A simple command for testing purposes. Obviously."""
    await interaction.response.send_message("Test")

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
        time.sleep(1/4) #not doing this results in the message not being sent and the bot erroring out.
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

@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def dice(interaction: nextcord.Interaction, diceamount: int, dicesides: int):  
    """Rolls the dice and returns the result in chat"""
    if (diceamount > 500): #more results in inconsistent errors
        await interaction.response.send_message("Whoa hey hold on! Thats way too many dice, I can't handle that! I only got enough hands for 500 of them!")
        return 
    if (dicesides > 500): #more results in inconsistent errors
        await interaction.response.send_message("I can't even find a dice with that many sides, keep it at 500 max.")
        return 
    if (dicesides == 1): #more results in inconsistent errors
        await interaction.response.send_message("Really now? " + str(diceamount) + " * 1? Didn't know I had to babysit a bunch of toddlers.")
        return 
    if (dicesides == 2): #more results in inconsistent errors
        resultsarray = []
        for i in range (diceamount):
            result = random.randint(1, 2)
            resultsarray.append(result)
        await interaction.response.send_message("Alright. I flipped " + str(diceamount) + " coins. The total result is " + str(sum(resultsarray)))
        resultsmessage = ("Individual results: " + str(resultsarray))
        if len(resultsmessage) >= 2000:
            resultarraysplit1 = resultsarraystring[:len(resultsarray)//2]
            resultsarraysplit2 = resultsarraystring[len(resultsarray)//2:]
            await interaction.followup.send("Individual results: ")
            await interaction.followup.send(resultarraysplit1)
            await interaction.followup.send(resultsarraysplit2)
        else:
            await interaction.followup.send(resultsmessage)
            return 
    amounttext = str(diceamount)
    sidestext = str(dicesides)
    diceresult = str(diceamount*random.randint(1, dicesides))
    resultsarray = []
    resultsarraystring = []
    for i in range (diceamount):
        result = random.randint(1, dicesides)
        resultsarray.append(result)    
        if (result == 1 or result == dicesides):
            text = str(result)
            boldtext = ("**" + text + "**")
            resultsarraystring.append(boldtext)
        else:
            resultsarraystring.append(str(result))
    await interaction.response.send_message("Rolled " + str(diceamount) + "d" + str(dicesides) + ". Result: " + str(sum(resultsarray)) + ".")
    resultsmessage = ("Individual results: " + str(resultsarraystring))
    if len(resultsmessage) >= 2000:
        resultarraysplit1 = resultsarraystring[:len(resultsarraystring)//2]
        resultsarraysplit2 = resultsarraystring[len(resultsarraystring)//2:]
        await interaction.followup.send("Individual results: ")
        await interaction.followup.send(resultarraysplit1)
        await interaction.followup.send(resultsarraysplit2)
    else:
        await interaction.followup.send(resultsmessage)

        

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

@client.command()
async def sen(ctx):
    if ctx.author.id == specialid:
        await ctx.send("amongus sussy plushy")
        await ctx.message.delete()
    else:
        await ctx.message.delete()


@client.event
async def on_message_delete(message):
    if (message.guild.id == ZeroSMServer):
        channel = client.get_channel(LogChannelID)
        author = str(message.author.nick)
        globalauthor = str(message.author.display_name)
        embed=nextcord.Embed(colour=nextcord.Colour.brand_red(), title="Deleted message from \n" + globalauthor, description = message.author.mention)
        embed.add_field(name="Message: ", value=message.content, inline=False)
        embed.add_field(name="In channel: ", value=message.channel, inline=False)
        if message.attachments:
            embed.set_image(message.attachments[0].url)
        await channel.send(embed=embed)

    
@client.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if (before.guild.id == ZeroSMServer):
        if (before.content != after.content):
            channel = client.get_channel(LogChannelID)
            author = str(before.author.nick)
            globalauthor = str(before.author.display_name)
            embed=nextcord.Embed(colour=nextcord.Colour.blue(), title="Edited message from \n" + globalauthor, description = before.author.mention)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            embed.add_field(name="Link to jump to message", value=after.jump_url, inline=False)
            if after.attachments or before.attachments:
                embed.set_image(after.attachments[0].url)
            await channel.send(embed=embed)

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send(ResponseArray[random.randint(0, len(ResponseArray)-1)])


@client.event
async def on_member_join(member):
    if (member.guild.id == ZeroSMServer):
        time.sleep(1)
        channel = client.get_channel(LogChannelID)
        day = str(member.created_at.day)
        month = str(member.created_at.month)
        year = str(member.created_at.year)
        embed=nextcord.Embed(color=nextcord.Colour.green(), title="New member joined", description= member.mention)
        embed.add_field(name="Member", value=member.global_name, inline=False)
        embed.add_field(name="Account created on", value=(day + "-" + month + "-" + year), inline=False)
        if member.display_avatar != None:
            embed.set_image(member.display_avatar)
        await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    if (member.guild.id == ZeroSMServer):
        time.sleep(1)
        channel = client.get_channel(LogChannelID)
        embed=nextcord.Embed(color=nextcord.Colour.blurple(), title="Member left")
        embed.add_field(name="Member", value=member.global_name, inline=False)
        embed.set_image(member.display_avatar)
        if member.display_avatar != None:
            embed.set_image(member.display_avatar)
        await channel.send(embed=embed)


@tasks.loop(seconds=300)
async def updatestatus():
    await client.change_presence(status=nextcord.Status.dnd, activity=nextcord.CustomActivity(StatusArray[random.randint(0, len(StatusArray)-1)]))

@client.event
async def on_ready():
    print("Bot is ready to do useful shit!\n")
    updatestatus.start()

client.run(BOTTOKEN)