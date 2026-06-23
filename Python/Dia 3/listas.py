
idades = [28, 42, 43, 35, 39, 28, 38, 42, 34]

print("soma idades: ", sum(idades))

print("soma idades: ", len(idades))

print("soma idades: ", sum(idades)/len(idades))

print("soma idades: ", min(idades))

print("soma idades: ", max(idades))

#leitra de outros tipos

eu = ["gabriel", 
      "davila", 
      3,
      ["LILIAN", "AUGUSTO", "ELIZABETH"], 
      "casado", 
      [1200, 2500, 3370 ,4750.33]]

print (eu[3][2])

filhos = eu[3]
primeiroFilho = filhos[0]
print(primeiroFilho)

tamanho = len(eu)
pos = tamanho - 3
filho = eu[pos][len(filhos) - 2]
print(filho)


filho2 = eu[3][-3]
print(filho2)

salario = eu[-1][-1]
print(salario)

salario = eu[5]
print(salario[::-1])

# eu [ start : stop ]