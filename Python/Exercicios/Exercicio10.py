lista = [1,2,3,3,2,1,1,1,1,1,5,6,7,7,6,5]
print("Esta é a lista: ", lista)

numero = input("entre com um numero:")
numero = int(numero)

contador = 0
for i in lista:
    if i == numero:
        contador = contador + 1

print("Quantidade de", numero, ":", contador)
