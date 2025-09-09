import random

def criar_baralho():
    naipes = ['♥', '♦', '♣', '♠']
    valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',]

    baralho = []
    for naipe in naipes :
        for valor in valores:
            baralho.append(f"{valor}{naipe}")
           
        return baralho
    
def embaralhar_baralho(baralho):
        random.shuffle(baralho)
        return baralho
     
def dar_carta(baralho):
    if not baralho:
        baralho = criar_baralho()
        embaralhar_baralho(baralho)

    carta = baralho.pop()
    return carta, baralho


def calcular_pontuacao(mao):
    pontuacao = 0
    num_ases = 0

    for carta in mao:
        valor = carta [:-1]

        if valor in ['J', 'Q', 'K']:
            pontuacao += 10
        elif valor == 'A':
            num_ases += 1
            pontuacao += 11
        else:
            pontuacao += int(valor)
        
    for _ in range(num_ases):
        if pontuacao + 11 <= 21:
            pontuacao += 11
        else:
            pontuacao += 1
       
    return pontuacao


