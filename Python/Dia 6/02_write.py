
txt = "Tese de escrita de historia de arquivo"

nomeArquivo = "historia02.txt"

# posso por como "A" para acrescentar no arquivo, ou "W" para sobrescrever o arquivo
with open(nomeArquivo, "w") as openFile:
    openFile.write(txt)
