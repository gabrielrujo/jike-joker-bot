import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN, PREFIX 
from games import girar_slots

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} está online! 🤡")

@bot.command()
async def versao(ctx):
    await ctx.send("🃏 Jike Joker Bot - Versão 1.0.0 🃏")

@bot.command()
async def joke(ctx):
    await ctx.send("Por que o palhaço levou uma escada para o bar? Porque ele ouviu que as bebidas estavam nas alturas! HIHAHIHA 🤡🍹")

@bot.command(name="slots", aliases=["slot", "s"])
async def slots(ctx):
    resultado, e_jackpot = girar_slots()
    resultado_str = " | ".join(resultado)

    await ctx.send(f" 🎰 Girando...🎰 \n [ {resultado_str} ]")

    if e_jackpot:
        await ctx.send("🎉 **JACKPOT!** 🎉")
    else:
        await ctx.send("HAHHAHAHAH PERDEU, PQ TA TAO SERIO? 🃏")



bot.run(DISCORD_TOKEN)