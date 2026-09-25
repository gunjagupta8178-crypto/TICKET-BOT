import discord, os
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Purchase", emoji="🛒", description="Kuch kharidne ke liye"),
            discord.SelectOption(label="Claim Rewards", emoji="🎁", description="Rewards claim karne ke liye"),
            discord.SelectOption(label="General Support", emoji="🎫", description="Help ke liye")
        ]
        super().__init__(placeholder="Select a ticket type...", options=options, custom_id="ticket_select")
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="TICKETS")
        if not category:
            category = await guild.create_category("TICKETS")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        channel = await guild.create_text_channel(name=f"{self.values[0].lower()}-{interaction.user.name}", category=category, overwrites=overwrites)
        await channel.send(f"{interaction.user.mention} Staff aayega!")
        await interaction.response.send_message(f"Ticket ban gaya: {channel.mention}", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot Online")

@bot.tree.command(name="ticketsetup", description="Ticket panel bhejo")
async def ticketsetup(interaction: discord.Interaction):
    embed = discord.Embed(title="UNION CLOUD - SUPPORT", description="🛒 **Purchase**\n🎁 **Claim Rewards**\n🎫 **General Support**\n\nNiche menu se select karo", color=0x9b59b6)
    await interaction.channel.send(embed=embed, view=TicketView())
    await interaction.response.send_message("Done", ephemeral=True)

bot.run(os.getenv("TOKEN"))
