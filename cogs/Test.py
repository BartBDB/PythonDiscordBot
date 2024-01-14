import discord
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #This is a test command. I use this to test any code quickly
    @commands.command()
    async def test(self, ctx): #don't forget to add self to this!!!
        await ctx.send("Test")
        await ctx.send(ctx.message.guild.name)
    
    @commands.command()
    async def ping(client, ctx):
        await ctx.send('Pong! {0}'.format(round(client.client.latency*1000, 1)))


async def setup(client):
    await client.add_cog(Test(client)) #this imports the cog into the bot

#command: @commands.command()
#event: @commands.Cog.listener()