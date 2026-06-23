
idades = []

while True:
    idade = input("entre com a idade: ")

    if idade == "":
        break

    idades.append(int(idade))

print("todas idades", idades)

mediaIdade = sum(idades) / len(idades)
minimoIdade = min(idades)
maximoIdade = max(idades)
qtdIdade = len(idades)

print("mediaIdade",mediaIdade)
print("minimoIdade",minimoIdade)
print("maximoIdade",maximoIdade)
print("qtdIdade",qtdIdade)