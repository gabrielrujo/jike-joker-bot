import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN, PREFIX 
from games.slots import girar_slots
from games.blackjack import criar_baralho, embaralhar_baralho, dar_carta, calcular_pontuacao

jogos_ativos = {}
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} está online! 🤡")

@bot.command()
async def versao(ctx):
    await ctx.send("🃏 Jike Joker Bot - Versão 1.1.0 ")

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


@bot.command(name="blackjack", aliases=["bj", "21"])
async def blackjack(ctx):
    if ctx.author.id in jogos_ativos:
        await ctx.send(f"Hahaha! Acha que pode jogar dois jogos ao mesmo tempo? Escolha um! Use {PREFIX}hit ou {PREFIX}stand para continuar a partida atual, ou caia fora! 🃏")
        return

    baralho = criar_baralho()
    baralho = embaralhar_baralho(baralho)

    
    carta_jogador1, baralho = dar_carta(baralho)
    carta_jogador2, baralho = dar_carta(baralho)
    mao_jogador = [carta_jogador1, carta_jogador2]

    
    carta_dealer1, baralho = dar_carta(baralho)
    carta_dealer2, baralho = dar_carta(baralho)
    mao_dealer = [carta_dealer1, carta_dealer2]

    
    jogos_ativos[ctx.author.id] = {
        "baralho": baralho,
        "mao_jogador": mao_jogador,
        "mao_dealer": mao_dealer
    }

    
    pontuacao_jogador = calcular_pontuacao(mao_jogador)
    pontuacao_dealer = calcular_pontuacao(mao_dealer)

   
    if pontuacao_jogador == 21 and pontuacao_dealer == 21:
        await ctx.send("Hahaha! A piada se repete. Que divertido! Ninguém venceu. 🤝")
        del jogos_ativos[ctx.author.id]
        return
    elif pontuacao_jogador == 21:
        await ctx.send("Uau, você teve sorte! **BLACKJACK!** Mas não se acostume... HAHAHAHA 🎉")
        del jogos_ativos[ctx.author.id]
        return
    elif pontuacao_dealer == 21:
        await ctx.send("HAHAHAHA! O dealer é o rei da piada aqui. Blackjack! Parece que o show acabou para você, camarada. 🃏")
        del jogos_ativos[ctx.author.id]
        return

    
    await ctx.send(f"Você recebeu: {', '.join(mao_jogador)} (Total: {pontuacao_jogador}). A mão do dealer é: {mao_dealer[0]} e uma carta virada para baixo.")


@bot.command(name="hit", aliases=["h"])
async def hit(ctx):
    if ctx.author.id not in jogos_ativos:
        await ctx.send(f"Você não está em um jogo de Blackjack no momento. Use {PREFIX}blackjack para iniciar um novo jogo. 🃏")
        return

    dados_jogo = jogos_ativos[ctx.author.id]
    mao_jogador = dados_jogo["mao_jogador"]
    baralho = dados_jogo["baralho"]

    nova_carta, baralho_atualizado = dar_carta(baralho)
    mao_jogador.append(nova_carta)

    pontuacao_jogador = calcular_pontuacao(mao_jogador)

    if pontuacao_jogador > 21:
        await ctx.send(f"Você pegou: {nova_carta}. Sua mão é: {', '.join(mao_jogador)} (Total: {pontuacao_jogador}).\nHAHAHA! Pobrezinho! Estourou. Ninguém gosta de perder, mas eu adoro ver! HAHAHA! 🤡")
        del jogos_ativos[ctx.author.id]
        return

    dados_jogo["mao_jogador"] = mao_jogador
    dados_jogo["baralho"] = baralho_atualizado

    await ctx.send(f"Você pegou: {nova_carta}. Sua mão agora é: {', '.join(mao_jogador)} (Total: {pontuacao_jogador}).")


@bot.command(name="stand", aliases=["st"])
async def stand(ctx):
    if ctx.author.id not in jogos_ativos:
        await ctx.send(f"Você não está em um jogo de Blackjack no momento. Use {PREFIX}blackjack para iniciar um novo jogo. 🃏")
        return

    dados_jogo = jogos_ativos[ctx.author.id]
    mao_jogador = dados_jogo["mao_jogador"]
    mao_dealer = dados_jogo["mao_dealer"]
    baralho = dados_jogo["baralho"]

    await ctx.send(f"A sua mão: {', '.join(mao_jogador)} (Total: {calcular_pontuacao(mao_jogador)}).")
    await ctx.send(f"O dealer revela sua segunda carta. A mão dele é: {', '.join(mao_dealer)} (Total: {calcular_pontuacao(mao_dealer)}).")

    while calcular_pontuacao(mao_dealer) < 17:
        nova_carta, baralho = dar_carta(baralho)
        mao_dealer.append(nova_carta)
        await ctx.send(f"O dealer pegou: {nova_carta}. A mão dele agora é: {', '.join(mao_dealer)} (Total: {calcular_pontuacao(mao_dealer)}).")

    pontuacao_dealer = calcular_pontuacao(mao_dealer)
    if pontuacao_dealer > 21:
        await ctx.send("HAHA! O dealer estourou! O show foi por água abaixo! Você venceu! 🎉")
    else:
        pontuacao_jogador = calcular_pontuacao(mao_jogador)
        if pontuacao_jogador > pontuacao_dealer:
            await ctx.send("Que tédio! Você venceu... A piada nem teve graça. 🎉")
        elif pontuacao_jogador < pontuacao_dealer:
            await ctx.send("HAHAHA! E a sua mão? Foi só uma piada! O dealer venceu! 🃏")
        else:
            await ctx.send("Ninguém venceu! Que palhaçada. A piada é que não teve piada. 🤝")

    del jogos_ativos[ctx.author.id]

bot.run(DISCORD_TOKEN)