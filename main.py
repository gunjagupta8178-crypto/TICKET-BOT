import discord, os
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Purchase", emoji="🛒", description="Purchase related"),
            discord.SelectOption(label="Claim Rewards", emoji="🎁", description="Claim rewards"),
            discord.SelectOption(label="General Support", emoji="📩", description="Support")
        ]
        super().__init__(placeholder="Select a ticket type...", options=options, custom_id="ticket_select")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="TICKETS")
        if not category:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
            category = await guild.create_category("TICKETS", overwrites=overwrites)
        
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category)
        await channel.set_permissions(interaction.user, view_channel=True, send_messages=True)
        await interaction.response.send_message(f"Ticket ban gaya! {channel.mention}", ephemeral=True)
        await channel.send(f"{interaction.user.mention} Support yaha karega!")

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot Online as {bot.user}")

@bot.tree.command(name="ticketsetup", description="Ticket panel bhejo")
async def ticketsetup(interaction: discord.Interaction):
    embed = discord.Embed(title="🎫 SUPPORT", description="Niche se ticket type select karo!", color=0x00ff00)
    await interaction.channel.send(embed=embed, view=TicketView())
    await interaction.response.send_message("Done", ephemeral=True)

keep_alive()
bot.run(os.getenv("TOKEN"))
