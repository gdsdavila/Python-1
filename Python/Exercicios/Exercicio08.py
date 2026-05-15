
saldoTotal = 0

while True:
    saldo = input("Entre com o Saldo ou ENTER para ver o saldo: ")
    if saldo == "":
        break

    saldoTotal = saldoTotal + float(saldo)

print("Saldo total: ", saldoTotal)
