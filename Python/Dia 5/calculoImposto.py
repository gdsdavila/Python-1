# *args são conjuntos ou tuplas(listas)
# **kwargs são dicionarios(dicionario - elementos nomeados que podem ser adicionados na invocação)

def calcImposto(preco:float, txBase:float, **kwargs):
    imposto = preco * txBase
    
    for i in kwargs:
        print(i, kwargs[i])
        imposto += preco * kwargs[i]

    return imposto

def valorTotal(preco:float, txBase:float, **kwargs):
    imposto = calcImposto(preco, txBase, **kwargs)
    return preco + imposto

impostosGerais = {
    "municipal":0.01,
    "estadual":0.005,
    "nacional":0.0001
 }

print("Imposto Total:", calcImposto(100, 0.03, **impostosGerais)) # posso adicionar um idependente se houver necessidade, após o **,# 
print("valor Total", valorTotal(100, 0.03, **impostosGerais))