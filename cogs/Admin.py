import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
from apikey import LogChannelID, ZeroSMMutedRole

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #kicking
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(client, ctx, member: discord.Member, *, reason=None):
        if reason == (None):
            reason = "No reason given."
        await ctx.send(f'User {member} has been **kicked**. Reason: '+ reason)
        channel = client.client.get_channel(LogChannelID)
        await channel.send((f"User {member} has been **kicked** by {client.client.get_user(ctx.author.id)}. Reason: " + reason))
        await member.send((f"You have been kicked from {ctx.message.guild.name}. Reason: " + reason))
        await member.kick(reason=reason)
        await ctx.message.delete()
    
    @kick.error
    async def kick_error(client, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to kick people. Nice try.")


    #banning
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(client, ctx, member: discord.Member, *, reason=None):
        if reason == (None):
            reason = "No reason given." 
        await ctx.send(f'User {member} has been **banned**. Reason: '+ reason)
        channel = client.client.get_channel(LogChannelID)
        await channel.send((f"User {member} has been **banned** by {client.client.get_user(ctx.author.id)}. Reason: " + reason))
        await member.send((f"You have been banned from {ctx.message.guild.name}. Reason: " + reason))
        await member.ban(reason=reason)
        await ctx.message.delete()

    @ban.error
    async def ban_error(client, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to ban people. Nice try.")
    
    #muting
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(client, ctx, member: discord.Member, *, reason=None):
        if reason == (None):
            reason = "No reason given." 
        else: 
            await ctx.send(f'User {member} has been **muted**. Reason: '+ reason)
            channel = client.client.get_channel(LogChannelID)
            await channel.send((f"User {member} has been **muted** by {client.client.get_user(ctx.author.id)}. Reason: " + reason))
            await member.send((f"You have been muted in {ctx.message.guild.name}. Reason: " + reason))
            await member.add_roles(ctx.guild.get_role(ZeroSMMutedRole))
            await ctx.message.delete()

    @mute.error
    async def mute_error(client, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to mute people. Nice try.")

async def setup(client):
    await client.add_cog(Admin(client)) #this imports the cog into the bot