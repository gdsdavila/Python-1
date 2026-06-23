
def jurosCompostos(saldo:int, taxa:float, anos:int):
    """
        função para calculo de juros compostos, levando em conta o SALDO, TAXA de juros e os ANOS que ficará rendendo
        SALDO:
            espera-se um valor inteiro
        
        TAXA:
            espera-se um valor com casas decimais

        ANOS:
            espera-se um valor inteiro
    """

    return saldo * (1 + taxa) ** anos

saldo = int(input("Digite o seu saldo: R$:"))
taxa = float(input("Qual a taxa atual? "))
anos = int(input("por quantos anos deseja? "))

print(jurosCompostos(saldo, taxa, anos))