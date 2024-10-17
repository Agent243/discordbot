import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import re
import os
from googlesearch import search

intents = discord.Intents.all()  # Activer toutes les intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Synchroniser les commandes slash
@bot.event
async def on_ready():
    await bot.tree.sync()  # Synchroniser les commandes slash avec Discord
    print(f"Connecté en tant que {bot.user} et prêt avec les commandes slash!")

# Liste de gros mots à interdire
french_swear_words = ["merde", "putain"]
english_swear_words = ["fuck", "shit"]
all_swear_words = french_swear_words + english_swear_words

# Message privé avec GIF (commande slash)
@bot.tree.command(name="send_dm", description="Envoyer un message privé avec un GIF")
async def send_dm(interaction: discord.Interaction, user: discord.User):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif') as r:
            if r.status == 200:
                gif_url = str(r.url)
                await user.send("Voici un petit GIF stylé pour toi!")
                await interaction.response.send_message(f"Message privé envoyé à {user.name}", ephemeral=True)

# Supprimer le message de l'auteur et répondre
@bot.tree.command(name="reply", description="Répondre tout en supprimant le message d'origine")
async def reply(interaction: discord.Interaction, message: str):
    await interaction.channel.send(f"{interaction.user.mention} a dit : {message}")
    await interaction.response.send_message("Votre message a été envoyé et supprimé", ephemeral=True)

# Voir la photo de profil d'un utilisateur
@bot.tree.command(name="avatar", description="Voir l'avatar d'un utilisateur")
async def avatar(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    await interaction.response.send_message(user.display_avatar.url)

# Rechercher sur Google
@bot.tree.command(name="google", description="Faire une recherche Google")
async def google(interaction: discord.Interaction, query: str):
    results = search(query, num_results=5)
    await interaction.response.send_message(f"Résultats pour '{query}':\n" + "\n".join(results))

# Lister les serveurs et membres
@bot.tree.command(name="servers", description="Lister les serveurs et leurs membres")
async def servers(interaction: discord.Interaction):
    server_info = ""
    for guild in bot.guilds:
        server_info += f"{guild.name} - {guild.member_count} membres\n"
    await interaction.response.send_message(f"Le bot est dans ces serveurs:\n{server_info}")

# Envoyer un message privé à un membre sans être ami
@bot.tree.command(name="send_pm", description="Envoyer un message privé à un utilisateur")
async def send_pm(interaction: discord.Interaction, user: discord.User, message: str):
    await user.send(message)
    await interaction.response.send_message(f"Message privé envoyé à {user.name}", ephemeral=True)

# Filtrer les gros mots
@bot.event
async def on_message(message):
    if any(swear in message.content.lower() for swear in all_swear_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, attention à ton langage!")
    await bot.process_commands(message)

# Shell interactif simple (à adapter pour sécurité)
@bot.tree.command(name="shell", description="Exécuter une commande shell")
async def shell(interaction: discord.Interaction, command: str):
    result = os.popen(command).read()
    await interaction.response.send_message(f"```\n{result}\n```")

# Ping une adresse IP
@bot.tree.command(name="ping", description="Pinger une adresse IP")
async def ping(interaction: discord.Interaction, ip: str):
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        await interaction.response.send_message(f"L'adresse {ip} est active.")
    else:
        await interaction.response.send_message(f"L'adresse {ip} ne répond pas.")

# Lancer le bot
bot.run('MTIzNTUyMDA0OTE4MDA1MzUxNQ.Gsq5-0.mNg734ijJ8pZm0lBq9Fgpjt2hcNg8D2csELeUA')
