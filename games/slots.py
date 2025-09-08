import random

def girar_slots():
    simbolos = ['🍒', '🍋', '🍊', '🃏', '⭐', '💎']
    
    roll1 = random.choice(simbolos)
    roll2 = random.choice(simbolos)
    roll3 = random.choice(simbolos)

    resultado = [roll1, roll2, roll3]

    if roll1 == roll2 == roll3:
        e_jackpot = True
    else:
        e_jackpot = False

    return resultado, e_jackpot