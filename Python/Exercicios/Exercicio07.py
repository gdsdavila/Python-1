soma = 0 # somatorio dos 4 valores

qtdeEntrada = 4 # quantas vezes terá a entrada do console

# como se voce tivesse 4 vidas e toda vez que o while rodar, uma vida será perdida.
# se ficar com zero, ele deixa de rodar(programa encontra o TRUE)

while qtdeEntrada > 0:
    altura = input("entre com a altura a ser somada: ")
    altura = float(altura)
    soma = soma + altura
    qtdeEntrada = qtdeEntrada - 1
print("soma das alturas: ", soma)