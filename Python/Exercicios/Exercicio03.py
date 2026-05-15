numero = input("Entre com um numero inteiro para saber a raiz quadrada: ")
numero = int(numero)

raiz = numero ** (1/2)
raiz = round(raiz, 4)

print("Raiz quadrada de ", numero, "é", raiz)