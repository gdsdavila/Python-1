soma = 0 # somatorio dos 4 valores

qtdeEntrada = 4 # quantas vezes terá a entrada do console

for i in range(qtdeEntrada): #range(0, 4)
    altura = input("entre com a altura a ser somada: ")
    altura = float(altura)
    soma = soma + altura

print("soma das alturas: ", soma)