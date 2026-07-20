
arquivo = "data.csv"

with open(arquivo) as open_file:
    data = open_file.readlines()

for linha in data:
    print(linha)

dados = dict()

chaves = data[0].strip("\n").split(";")
print(chaves)