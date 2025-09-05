import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN, PREFIX 

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} está online! 🤡")

@bot.command()
async def ping(ctx):
    await ctx.send("pong 🏓")

bot.run(DISCORD_TOKEN)