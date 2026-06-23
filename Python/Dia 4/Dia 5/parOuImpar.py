
def parImpar(numero:int):
    if numero % 2 == 0:
        return "é par"
    
    else:
        return "é impar"

numero = int(input("Entre com um numero"))

resultado = parImpar(numero)

print("o valor", numero, resultado)