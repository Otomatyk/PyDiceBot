import discord
from discord.ext import commands
from dice_engine_core import exec_commande
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="h!", intents=intents)

srlist = []

@bot.event
async def on_message(message):
    try:
        if message.content == "!sr":
            if srlist.count(message.author.id) == 0:
                srlist.append(message.author.id)
                await message.channel.send("```!SR Activé```")
                
            else:
                srlist.remove(message.author.id)
                await message.channel.send("```!SR Désactivé```")

        elif message.content.startswith("!"):
            await message.channel.send(exec_commande(message.content))
            
    except IndexError as erreur:
        print(erreur)
        print("Commande slash utilisé")
              
bot.run('Token du bot ici')
