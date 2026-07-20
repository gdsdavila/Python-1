nomeArquivo = "historia.txt"

#abre o arquivo como leitura
openFile = open(nomeArquivo)

#le os dados do arquivo
conteudo = openFile.read()
print(conteudo)

# fecha o arquivo
openFile.close()

#OU o modo mais facil e mais feito!!

with open(nomeArquivo) as openFile:
    conteudo = openFile.read()

print(conteudo)