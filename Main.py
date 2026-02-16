import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    async def on_ready(self): #boots up
        print(f'logged on as {self.user}')

        await client.change_presence(activity=discord.Game(name="11 Amigos bot"))

        try:
            guild = discord.Object(id=1364228769690419282) # force setup cmd
            synced = await self.tree.sync(guild=guild)
            print(f'successfully synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'error syncing cmd: {e}') #if it fails send an error message

    async def on_message(self, message): #when someone messages
        print(f'message from {message.author}: {message.content}')

        if message.content.startswith('stupid bot'): #message contains stupid bot
            await message.channel.send(f'hey thats not nice {message.author}!') #say hey thats not nice

intents = discord.Intents.default() #intents is basically what the bot can do
intents.message_content = True
client = Client(command_prefix="/", intents=intents)

guildid = discord.Object(id=1364228769690419282) #where you want the slash commands to be

@client.tree.command(name='hey', description='Say hi!', guild=guildid) #creating slash commands
async def Hey(interaction: discord.interactions): #on run
    await interaction.response.send_message(f"Hello {interaction.user.mention}!") #reply to person that ran command and say hi

@client.tree.command(name="repeater", description="repeats parameter provided", guild=guildid)
async def repeater(interaction: discord.interactions, text: str, repeat: int):

    if repeat > 10:
        await interaction.response.send_message('Error: cannot repeat more than 10 times')
        return

    await interaction.response.defer()

    for _ in range(repeat):
        await interaction.followup.send(text)
client.run('MTQ1OTczODYxODE3MTA5NzEzMQ.GrdDu2.TekNCPG39akGtsDXsJ08urShji2a7cGxgELJL4') #token to let the bot boot up