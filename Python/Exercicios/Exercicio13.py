
frases = {}

while True:
    frase = input("Entre com a frase desejada(enter para sair): ")
    if frase == "":
        break

    if frase not in frases:
        frases[frase] = 1

    else:
        frases[frase] += 1

for i, j in frases.items():
    print(i, "->", j)