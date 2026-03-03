import random

numero= int(input("Digite um valor inteiro de 1 a 10: "))

valor= random.randint(1, 10)


if(numero==valor):
    print("Você acertou, o valor sorteado foi:", valor)

while(numero!= valor):
      print("Tente novamente")
      numero= int(input("Digite um valor inteiro de 1 a 10: "))


print("Valor sorteado:", valor)  

