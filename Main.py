import discord
import time
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

class Client(commands.Bot):
    # boot function
    async def on_ready(self):
        print(f'logged on as {self.user}')

        await client.change_presence(activity=discord.Game(name="11 Amigos bot"))

        # setting up commands
        try:
            guild = discord.Object(id=1364228769690419282)
            synced = await self.tree.sync(guild=guild)
            print(f'successfully synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'error syncing cmd: {e}')

    # on message func
    async def on_message(self, message):
        print(f'message from {message.author}: {message.content}')

        if message.content.startswith('stupid bot'):
            await message.channel.send(f'hey thats not nice {message.author}!')
    
    # reaction add func
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        guild = reaction.message.guild
        if not guild:
            return
        if hasattr(self, "colour_role_message_id") and reaction.message.id != self.colour_role_message_id:
            return
        
        emoji = str(reaction.emoji)

        reaction_role_map = {
            '❤️': 'Red',
            '💙': 'Blue',
            '💚': 'Green',
            '💛': 'Yellow',
            '🧡': 'Orange',
            '💜': 'Purple',
            '🩵': 'Cyan',
            '🩶': 'Gray',
            '🤍': 'White',
            '🖤': 'Black',
            '🍋‍🟩': 'Lime'
        }

        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            if role and user:
                await user.add_roles(role)
    

    # reaction remove func
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return 
        guild = reaction.message.guild
        if not guild:
            return 
        if hasattr(self, "colour_role_message_id") and reaction.message.id != self.colour_role_message_id: 
            return
        
        emoji = str(reaction.emoji)
        reaction_role_map = {
            '❤️': 'Red',
            '💙': 'Blue',
            '💚': 'Green',
            '💛': 'Yellow',
            '🧡': 'Orange',
            '💜': 'Purple',
            '🩵': 'Cyan',
            '🩶': 'Gray',
            '🤍': 'White',
            '🖤': 'Black',
            '🍋‍🟩': 'Lime'
        }

        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji] 
            role = discord.utils.get(guild.roles, name=role_name)

            if role and user:
                await user.remove_roles(role)

# intents (basicaly permissions)
intents = discord.Intents.default()
intents.reactions = True
intents.guilds = True
intents.members = True
intents.message_content = True
client = Client(command_prefix="/", intents=intents)

# guild initialization (guild is server (this is to run the commands))
guildid = discord.Object(id=1364228769690419282)

# hey command
@client.tree.command(name='hey', description='Say hi!', guild=guildid)
async def Hey(interaction: discord.interactions):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

# embed cmd
@client.tree.command(name='embed', description='embed test', guild=guildid)
async def embedder(interaction: discord.interactions):
    embed = discord.Embed(title="click me, I dare you", description="Embed test: Description", url="https://www.youtube.com", color=discord.Color.blue())
    embed.set_thumbnail(url="https://picsum.photos/200")
    embed.add_field(name="Field title: Test", value="Field value: Test")
    embed.set_footer(text="Footer: Test")
    embed.set_author(name=interaction.user, url="https://www.youtube.com", icon_url="https://picsum.photos/200")
    await interaction.response.send_message(embed=embed)

# button setting up
class View(discord.ui.View):
    @discord.ui.button(label="Test", style=discord.ButtonStyle.blurple, emoji="🔥")
    async def button_callback(self, button, interaction):
        await button.response.send_message("You clicked the button!")

# button cmd
@client.tree.command(name='button', description='Creates a button', guild=guildid)
async def button(interaction: discord.interactions):
    await interaction.response.send_message(view=View())

# repeater cmd
@client.tree.command(name="repeater", description="repeats parameter provided", guild=guildid)
async def repeater(interaction: discord.interactions, text: str, repeat: int):

    if repeat > 10:
        await interaction.response.send_message('Error: cannot repeat more than 10 times')
        return

    await interaction.response.defer()

    for _ in range(repeat):
        await interaction.followup.send(text)

 # Option dropdown setting up
class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Test Option",
                description="Description: Test",
                emoji="👋"
            ),
            discord.SelectOption(
                label="Option 2",
                description="description 2",
                emoji="💬"
            )
        ]
        
        super().__init__(placeholder="Choose an option:", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Test Option":
            await interaction.response.send_message(f"You picked option 1")
        elif self.values[0] == "Option 2":
            await interaction.response.send_message(f"You picked option 2")
        

# actually making the menu work
class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

# menu command setting up
@client.tree.command(name='menu', description='Display a dropdown menu', guild=guildid)
async def menu(interaction: discord.interactions):
    await interaction.response.send_message(view=MenuView())


# reaction role command

@client.tree.command(name="colourroleembed", description="Creates an embed that allows you to react with the colour that you want", guild=guildid)
async def colourrole(interaction: discord.interactions):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Error: You have to be an admin to run this command!", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)

    Description=(
    "React to this message to chose your name colour \n\n"
    "❤️ Red\n"
    "💚 Green\n"
    "💙 Blue\n"
    "💛 Yellow\n"
    "🧡 Orange\n"
    "💜 Purple\n"
    "🩵 Cyan\n"
    "🩶 Gray\n"
    "🖤 Black\n"
    "🤍 White\n"
    "🍋‍🟩 Lime")

    embed = discord.Embed(title="Choose your name colour", description=Description, color=discord.Color.blue())
    message = await interaction.channel.send(embed=embed)
    
    emojis = ['❤️','💚','💙','💛','🧡','💜','🩵','🩶','🖤','🤍','🍋‍🟩']

    for emoji in emojis:
        await message.add_reaction(emoji)
    
    client.colour_role_message_id = message.id

    await interaction.followup.send("Colour role message sucessfully created!", ephemeral=True)

# bot token
client.run(TOKEN)
