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

#Thisll be done soon i swear
#def create_embed(embedtitle, membermention, interactionuserid, interactionusername, membername, memberid, reason, hasavatar, displayavatar):
#    channel = client.get_channel(LogChannelID)
#    listchannel = client.get_channel(ListChannelID)
#    embed=nextcord.Embed(color=nextcord.Colour.dark_red(), title=embedtitle, description=membermention)
#    embed.add_field(name="Action applied by", value=str(interactionuserid) + ", " + interactionusername, inline=False)
#    embed.add_field(name="Member", value=membername, inline=False)
#    embed.add_field(name="User ID", value=memberid, inline=False)
#    embed.add_field(name="Reason", value=reason, inline=False)
#    if hasavatar == True:
#        embed.set_thumbnail(displayavatar)
#    listchannel.send(embed=embed)
#    channel.send(embed=embed)
    

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
    if not os.path.isdir(hugfilepath):
        await interaction.response.send_message("How odd, I can't find the images. Tell Zev he messed up.")
        return
    if integer == 10:
        await interaction.response.send_message("Sending you a hug!", files=[nextcord.File(hugfilepath + '/hugs.gif')])
    else:
        await interaction.response.send_message("Sending you a hug!", files=[nextcord.File(hugfilepath + '/hug.gif')])


#kick command and error
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
@application_checks.has_permissions(kick_members=True)
async def kick(interaction: nextcord.Interaction, member: nextcord.Member, reason=None):
    """Makes Closure kick a member out of the server."""
    if reason == (None):
        reason = "No reason given."
    await interaction.response.send_message(f'User **{member}** has been **kicked**. Reason: '+ reason)
    channel = client.get_channel(LogChannelID)
    listchannel = client.get_channel(ListChannelID)
    embed=nextcord.Embed(color=nextcord.Colour.dark_red(), title="User has been kicked", description= member.mention)
    embed.add_field(name="Action applied by", value=str(interaction.user.id) + ", " + interaction.user.name, inline=False)
    embed.add_field(name="Member", value=member.name, inline=False)
    embed.add_field(name="User ID", value=member.id, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    if member.display_avatar != None:
        embed.set_thumbnail(member.display_avatar)
    await listchannel.send(embed=embed)
    await channel.send(embed=embed)
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
    listchannel = client.get_channel(ListChannelID)
    embed=nextcord.Embed(color=nextcord.Colour.dark_red(), title="User has been banned", description= member.mention)
    embed.add_field(name="Action applied by", value=str(interaction.user.id) + ", " + interaction.user.name, inline=False)
    embed.add_field(name="Member", value=member.name, inline=False)
    embed.add_field(name="User ID", value=member.id, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    if member.display_avatar != None:
        embed.set_thumbnail(member.display_avatar)
    await listchannel.send(embed=embed)
    await channel.send(embed=embed)
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
        listchannel = client.get_channel(ListChannelID)
        embed=nextcord.Embed(color=nextcord.Colour.dark_red(), title="User has been muted", description= member.mention)
        embed.add_field(name="Action applied by", value=str(interaction.user.id) + ", " + interaction.user.name, inline=False)
        embed.add_field(name="Member", value=member.name, inline=False)
        embed.add_field(name="User ID", value=member.id, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        if member.display_avatar != None:
            embed.set_thumbnail(member.display_avatar)
        await listchannel.send(embed=embed)
        await channel.send(embed=embed)
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
    listchannel = client.get_channel(ListChannelID)
    embedtitle = ""
    if reason == (None):
        reason = "No reason given." 
    if member.get_role(Strike2):
        await interaction.response.send_message(f'User **{member}** has been **warned a third time and got banned**. Reason: '+ reason)
        await member.send((f"You have been **warned three times and got banned** from **{interaction.guild.name}**. Reason: " + reason))
        time.sleep(1/4) #not doing this results in the message not being sent and the bot erroring out.
        await member.ban(reason=reason)
        embedtitle = "Ban due to 3rd strike"
    elif member.get_role(Strike1):
        await interaction.response.send_message(f'User **{member}** has been **warned a second time**. Reason: '+ reason)
        await member.send((f"You have been **warned twice** in **{interaction.guild.name}**. Any further strikes will result in a ban from the server. Reason: " + reason))
        time.sleep(1/4) #maybe this fixes the weird bug im having with the second strike specifically?
        await member.add_roles(interaction.guild.get_role(Strike2))
        embedtitle = "Second strike applied"
    else:  
        await interaction.response.send_message(f'User **{member}** has been **warned once**. Reason: '+ reason)
        await member.send((f"You have been **warned once** in **{interaction.guild.name}**. Reason: " + reason))
        await member.add_roles(interaction.guild.get_role(Strike1))
        embedtitle = "First strike applied"

    #Send a message in the list channel
    embed=nextcord.Embed(color=nextcord.Colour.dark_red(), title=embedtitle, description= member.mention)
    embed.add_field(name="Action applied by", value=str(interaction.user.id) + ", " + interaction.user.name, inline=False)
    embed.add_field(name="Member", value=member.name, inline=False)
    embed.add_field(name="User ID", value=member.id, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    if member.display_avatar != None:
        embed.set_thumbnail(member.display_avatar)
    await listchannel.send(embed=embed)
    await channel.send(embed=embed)


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
    if (dicesides == 1): 
        await interaction.response.send_message("Really now? " + str(diceamount) + " * 1? Didn't know I had to babysit a bunch of toddlers.")
        return 
    if (dicesides == 2): 
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
    if (diceamount > 1):
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
    #userroles = message.author.roles
    mod = get(message.guild.roles, id=Modrole)
    admin = get(message.guild.roles, id=Adminrole)
    fool = get(message.guild.roles, id=Fool)
    #send something in the chat when mentioned with special lines for mods and higher only
    if client.user.mentioned_in(message) and message.mention_everyone == False:
        #if mod in userroles or admin in userroles or fool in userroles:
            #await message.channel.send(modresponsearray[random.randint(0, len(modresponsearray)-1)])
        #else:
        await message.channel.send(ResponseArray[random.randint(0, len(ResponseArray)-1)])

    #TODO - Check for invites
        
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
            embed.set_thumbnail(member.display_avatar)
        await loggingchannel.send(embed=embed)


@client.event
async def on_member_remove(member):
    if (member.guild.id == ZeroSMServer):
        time.sleep(1)
        embed=nextcord.Embed(color=nextcord.Colour.blurple(), title="Member left")
        embed.add_field(name="Member", value=member.name, inline=False)
        if member.display_avatar != None:
            embed.set_thumbnail(member.display_avatar)
        await loggingchannel.send(embed=embed)


@client.event
async def on_message_bulk_delete(messages):
    if (messages.guild.id == ZeroSMServer):
        embed=nextcord.Embed(color=nextcord.Colour.blurple(), title="Messages have been purged")
        embed.add_field(name="Amount of messages", value=len(messages), inline=False)
        embed.add_field(name="Channel", value=messages[0].channel, inline=False)
        await loggingchannel.send(embed=embed)


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
#@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
#async def test(interaction: nextcord.Interaction):
#    """A simple command for testing purposes. Obviously."""
#    test = client.get_emoji(1193136758427242536)
#    provenceemoji = nextcord.PartialEmoji.from_str(str(test))
#    await interaction.response.send_message(provenceemoji)


#Music related stuff
import yt_dlp as youtube_dl
import asyncio

client.queue = []
client.sentqueue = []
client.queuemoved = False

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream)) 

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(source=filename, executable="ffmpeg", pipe=False, stderr=None, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn"), data=data)

@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def play(interaction: nextcord.Interaction, url: str):
    """Plays a link supported by yt-dl. This is streamed over the network so yell at Zev if it breaks"""
    await interaction.response.defer()
    for i in client.voice_clients:
        #print(i.is_playing())
        if i.is_playing():
            player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
            client.queue.append(player)         
            await interaction.followup.send("Added " + str(player.title) + " to the queue. - <" + url + ">")
        else:
            player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
            i.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )    
            client.queue.append(player)
            await interaction.followup.send("Now playing: " + str(player.title) + " - <" + url + ">")
        #print(client.queue)

@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def queue(interaction: nextcord.Interaction):
    """Shows the current queue, if any"""
    await interaction.response.defer()
    if len(client.queue) > 0:
        client.sentqueue.clear()
        for i in client.queue:          
            client.sentqueue.append(i.title)
        await interaction.followup.send(client.sentqueue)
    else:
        await interaction.followup.send("The queue is empty!")

@tasks.loop(seconds=5) #This is kinda ugly right now but since it only runs music for one server it will be fine
async def updatequeue():
    if client.voice_clients:
        for i in client.voice_clients:
            if i.is_playing() and (len(client.queue) > 1) and client.queuemoved == False:
                client.queue.pop(0) #NOT REMOVE! Remove needs a specified value, pop just needs an integer
                client.queuemoved = True
            if (i.is_playing() == False) and (len(client.queue) >= 1) and client.queuemoved == True:
                i.play(
                    client.queue[0], after=lambda e: print(f"Player error: {e}") if e else None
                )
                client.queuemoved = False

#https://www.youtube.com/watch?v=sJC447aP7yg
#https://www.youtube.com/watch?v=Cr_hpsBXlDc

@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def join(interaction: nextcord.Interaction, channel: nextcord.VoiceChannel):
    """Makes Closure join a voice channel"""
    await channel.connect()
    await interaction.response.send_message("Joining voice channel " + str(channel) + "!")
    
@client.slash_command(guild_ids=[TestServer, ZeroSMServer])
async def leave(interaction: nextcord.Interaction):
    """Makes Closure leave the voice channel. Message a mod if Closure isn't properly leaving the channel"""
    for i in client.voice_clients:
        await i.disconnect()
    await interaction.response.send_message("Leaving the voice channel!")

@client.event
async def on_ready():
    updatestatus.start()
    updatequeue.start()
    global modresponsearray 
    modresponsearray = ResponseArray + ModArray
    global loggingchannel
    loggingchannel = client.get_channel(LogChannelID)
    print("Bot is ready to do useful shit!\n")

client.run(BOTTOKEN)