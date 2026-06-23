# dicionario são pares de chaves associados a um valor(chave/valor são pares)

dadosEu = {
           "nome":"gabriel",
           "idade":"29",
           "filhos":False,
           "formacao":["ADS", "ELETRONICA"], #valor é uma lista
           "cargos":[                        #valor é lista de dicionarios
               {"nome":"ADS", "teste":"empresa"},
               {"nome":"teste", "teste":"empresa1"},
               {"nome":"maluko", "teste":"empresa2"},
               {"nome":"3d", "teste":"empresa3"}
            ]
}

print(dadosEu["formacao"][-1])
print(dadosEu["cargos"][-1]["teste"])

# criar uma nova chave
dadosEu["estado civil"] = "casado"

print(dadosEu)
print()

# descobrondo o nome das chaves deste dicionario
print("chaves:", dadosEu.keys())

# descobrir os valores de cada chaves
print()
print("valores:", dadosEu.values())

# Itens do dicionario
print()
print("Itens:", dadosEu.items())

# utilizando o for

for chave in dadosEu:
    print(chave, "->" ,dadosEu[chave])


for item in dadosEu.items():
    print(item)

for [chave, valor] in dadosEu.items():
    print(chave, "->", valor)