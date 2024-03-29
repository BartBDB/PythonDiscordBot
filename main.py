import nextcord
from nextcord import Interaction
from nextcord.utils import get
from nextcord.ext import commands, tasks
from nextcord.ext import application_checks
from apikey import *
import random
import os
import time
import sys

#Intents
intents = nextcord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='&', intents=nextcord.Intents.all())

#ping command
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def ping(interaction: nextcord.Interaction):
    """Pings Closure and sends her response time back in ms."""
    await interaction.response.send_message('Pong! {0}'.format(round(client.latency*1000, 1)))


#test command
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def hug(interaction: nextcord.Interaction):
    """Ask Closure to send a hug. She's using a terminal in Terra so she can't physically do it"""
    integer = random.randint(1, 10)
    if not os.path.isdir('images/hug'):
        await interaction.response.send_message("How odd, I can't find the images. Tell Zev he messed up.")
        return
    if integer == 10:
        await interaction.response.send_message("Sending you a hug!", files=[nextcord.File('images/hug/hugs.gif')])
    else:
        await interaction.response.send_message("Sending you a hug!", files=[nextcord.File('images/hug/hug.gif')])


#kick command and error
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
@application_checks.has_permissions(kick_members=True)
async def kick(interaction: nextcord.Interaction, member: nextcord.Member, reason=None):
    """Makes Closure kick a member out of the server."""
    if reason == (None):
        reason = "No reason given."
    await interaction.response.send_message(f'User **{member}** has been **kicked**. Reason: '+ reason)
    channel = client.get_channel(LogChannelID)
    await channel.send((f"User **{member}** has been **kicked** by **{interaction.user.name}**. Reason: " + reason))
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
    await channel.send((f"User **{member}** has been **banned** by **{interaction.user.name}**. Reason: " + reason))
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
        await channel.send((f"User **{member}** has been **muted** by **{interaction.user.name}**. Reason: " + reason))
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
        await channel.send((f"User **{member}** has been **warned a third time and got banned** by **{interaction.user.name}**. Reason: " + reason))
        await member.send((f"You have been **warned three times and got banned** from **{interaction.guild.name}**. Reason: " + reason))
        time.sleep(1/4) #not doing this results in the message not being sent and the bot erroring out.
        await member.ban(reason=reason)
    elif member.get_role(Strike1):
        await interaction.response.send_message(f'User **{member}** has been **warned a second time**. Reason: '+ reason)
        await channel.send((f"User **{member}** has been **warned a second time** by **{interaction.user.name}**. Reason: " + reason))
        await member.send((f"You have been **a second time** in **{interaction.guild.name}**. Reason: " + reason))
        await member.add_roles(interaction.guild.get_role(Strike2))
    else:  
        await interaction.response.send_message(f'User **{member}** has been **warned once**. Reason: '+ reason)
        await channel.send((f"User **{member}** has been **warned once** by **{interaction.user.name}**. Reason: " + reason))
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
            resultsarraysplit1 = resultsarraystring[:len(resultsarray)//2]
            split1 = resultsarraysplit1.replace("'", "")
            resultsarraysplit2 = resultsarraystring[len(resultsarray)//2:]
            split2 = resultsarraysplit2.replace("'", "")
            await interaction.followup.send("Individual results: ")
            await interaction.followup.send(split1)
            await interaction.followup.send(split2)
        else:
            result = resultsmessage.replace("'", "")
            await interaction.followup.send(result)
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
        resultsarraysplit1 = resultsarraystring[:len(resultsarraystring)//2]
        strsplit1 = str(resultsarraysplit1)
        split1 = strsplit1.replace("'", "")
        resultsarraysplit2 = resultsarraystring[len(resultsarraystring)//2:]
        strsplit2 = str(resultsarraysplit2)
        split2 = strsplit2.replace("'", "")
        await interaction.followup.send("Individual results: ")
        await interaction.followup.send(split1)
        await interaction.followup.send(split2)
    else:
        result = resultsmessage.replace("'", "")
        await interaction.followup.send(result)


@client.event
async def on_message_delete(message):
    if (message.guild.id == ZeroSMServer):
        author = str(message.author.nick)
        globalauthor = str(message.author.display_name)
        embed=nextcord.Embed(colour=nextcord.Colour.brand_red(), title="Deleted message from \n" + globalauthor, description = message.author.mention)
        embed.add_field(name="Message: ", value=message.content, inline=False)
        embed.add_field(name="In channel: ", value=message.channel, inline=False)
        if message.attachments:
            image = message.attachments[0].proxy_url
            embed.set_image(image)
        await loggingchannel.send(embed=embed)

    
@client.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if (before.guild.id == ZeroSMServer):
        if (before.content != after.content):
            globalauthor = str(before.author.name)
            embed=nextcord.Embed(colour=nextcord.Colour.blue(), title="Edited message from \n" + globalauthor, description = before.author.mention)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            embed.add_field(name="Link to jump to message", value=after.jump_url, inline=False)
            if after.attachments or before.attachments:
                embed.set_image(after.attachments[0].url)
            await loggingchannel.send(embed=embed)


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        userroles = message.author.roles
        mod = get(message.guild.roles, id=Modrole)
        admin = get(message.guild.roles, id=Adminrole)
        fool = get(message.guild.roles, id=Fool)
        if mod in userroles or admin in userroles or fool in userroles:
            await message.channel.send(modresponsearray[random.randint(0, len(modresponsearray)-1)])
        else:
            await message.channel.send(ResponseArray[random.randint(0, len(ResponseArray)-1)])


@client.event
async def on_member_join(member):
    if (member.guild.id == ZeroSMServer):
        time.sleep(1)
        day = str(member.created_at.day)
        month = str(member.created_at.month)
        year = str(member.created_at.year)
        embed=nextcord.Embed(color=nextcord.Colour.green(), title="New member joined", description= member.mention)
        embed.add_field(name="Member", value=member.name, inline=False)
        embed.add_field(name="Account created on", value=(day + "-" + month + "-" + year), inline=False)
        if member.display_avatar != None:
            embed.set_image(member.display_avatar)
        await loggingchannel.send(embed=embed)


@client.event
async def on_member_remove(member):
    if (member.guild.id == ZeroSMServer):
        time.sleep(1)
        embed=nextcord.Embed(color=nextcord.Colour.blurple(), title="Member left")
        embed.add_field(name="Member", value=member.name, inline=False)
        embed.set_image(member.display_avatar)
        if member.display_avatar != None:
            embed.set_image(member.display_avatar)
        await loggingchannel.send(embed=embed)

#bad bad bad BAAAAAD IDEA
#@client.event
#async def on_error(error):
#    #await loggingchannel.send(error)
#    await os.execv(sys.executable, ['python'] + sys.argv)


@tasks.loop(seconds=300)
async def updatestatus():
    #test = client.get_emoji(1193136758427242536)
    #provenceemoji = nextcord.PartialEmoji.from_str(str(test))
    await client.change_presence(status=nextcord.Status.dnd, activity=nextcord.CustomActivity(name = (StatusArray[random.randint(0, len(StatusArray)-1)])))#, emoji = provenceemoji))


@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def restart(interaction: nextcord.Interaction):
	"""Restarts Closure's terminal. Only usable by ZeverousNova"""
	if interaction.user.id == ID:
		await interaction.response.send_message("Alright, restarting the terminal.")
		await os.execv(sys.executable, ['python'] + sys.argv)
	else:
		await interaction.response.send_message("Yeah, not happening.")


@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def shutdown(interaction: nextcord.Interaction):
	"""Shuts down Closure's terminal. Only usable by ZeverousNova"""
	if interaction.user.id == ID:
		await interaction.response.send_message("Shutting down the terminal. Don't forget to restart the pi.")
		exit()
	else:
		await interaction.response.send_message("Nuh uh")


#test command
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def test(interaction: nextcord.Interaction):
    """A simple command for testing purposes. Obviously."""
    test = client.get_emoji(1193136758427242536)
    provenceemoji = nextcord.PartialEmoji.from_str(str(test))
    await interaction.response.send_message(provenceemoji)


@client.event
async def on_ready():
    updatestatus.start()
    global modresponsearray 
    modresponsearray = ResponseArray + ModArray
    global loggingchannel
    loggingchannel = client.get_channel(LogChannelID)
    print("Bot is ready to do useful shit!\n")

client.run(BOTTOKEN)


#Random message
#@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
#async def randommessage(interaction: nextcord.Interaction,):
#	"""Grabs a random message from this channel"""
#	array = []
#	async for message in interaction.channel.history(limit=500):
#		array.append(message)
#	integer = random.randint(0, 500)
#	await interaction.response.send_message(str(array[integer].author) + ": " + array[integer].content)
#	await interaction.followup.send(array[integer].jump_url)
