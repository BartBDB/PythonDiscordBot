import discord
from discord.ext import commands
from apikey import ID

class Say(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx):
        if ctx.author.id == ID:
            msg = ctx.message.content
            msgtosend = msg.replace("&say ", "")
            await ctx.send(msgtosend)
            await ctx.message.delete()
        else:
            await ctx.send("This command is only usable by the bot owner, ZeverousNova")

async def setup(client):
    await client.add_cog(Say(client))