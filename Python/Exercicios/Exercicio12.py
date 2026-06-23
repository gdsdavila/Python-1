frutas = {"maça":1.50, 
          "pera":1.25, 
          "goiaba":2.15, 
          "banana":2.75, 
          "laranja":0.65, 
          "abacaxi":3.20, 
          "uva":1.90, 
          "limao":1.25, 
          "jaca":5.80}

selectFrutas = input("Qual fruta você deseja? ")

if selectFrutas in frutas:
    print("fruta: ", selectFrutas, "valor: R$:", frutas[selectFrutas])

else:
    print("Entre com o valor valido")