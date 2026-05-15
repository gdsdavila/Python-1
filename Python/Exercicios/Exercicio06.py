#texto = """
#Qual tipo você deseja? 
#(1) - natural  (2) - com gás
#"""
#opcao = int(input(texto))

#if opcao == 1:
#    quantidade = int(input("Quantas garrafas?"))
#    total = quantidade * 1
#    print("Total da compra: R$:", total, "Reais")


#elif opcao == 2:
#    quantidade = int(input("Quantas garrafas?"))
#    total = quantidade * 1.5
#    print("Total da compra: R$:", total, "Reais")

#else:
#    print("entre com um valor valido!!")



# outro modo
texto = """
Qual tipo você deseja? 
(1) - natural R$:1.5
(2) - com gás R$:2.5
"""
opcao = input(texto)

valor_item = 0
if opcao == "1":
    valor_item = 1.5

elif opcao == "2":
    valor_item = 2.5

if valor_item == 0:
    print("entre com o valor correto")

else:
    qtde = int(input("quantas garrafas deseja?"))

    valor_total = valor_item * qtde

    print("sua conta é R$: ", valor_total)