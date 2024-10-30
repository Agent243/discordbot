import discord
from discord.ext import commands
from googletrans import Translator

# Initialise le bot avec le préfixe que tu préfères (par exemple, "!")
bot = commands.Bot(command_prefix="!")

# Initialise le traducteur
translator = Translator()

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    # Empêche le bot de répondre à lui-même
    if message.author == bot.user:
        return

    # Traduit le contenu du message en français
    translated = translator.translate(message.content, dest="fr")
    
    # Envoie le texte traduit dans le même canal
    await message.channel.send(f"**Traduction en français :** {translated.text}")

    # Permet au bot de traiter d'autres commandes si nécessaire
    await bot.process_commands(message)

# Lance le bot avec le token
bot.run("MTIyNzIyMjk5MDE4MjQyMDYwMA.GUOlb_.HcP9coLyWJBSM_DcDFaft9L5jztBuxaUTR3Zys")
