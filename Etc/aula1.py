print("Programação Orientada a Objetos")

nome= input("Nome: ")
idade= input("Idade: ")
idade= int(idade)
salario=float(input("Salário: "))


print("Olá", nome, "você tem", idade, "anos.")
# str formatada
print(f"Olá {nome}. Você tem {idade} anos. ")
salario
print(f"Você ganha muito mal:", salario)
if(salario<=10000):
    print(f"Você ganha muito mal: R$ {salario:.2f}")
elif(salario>10000 and salario<=20000):
    print(f"Você ganha bem: R$ {salario:.2f}")
else:
 print(f"Você ganha muito bem: R$ {salario:.2f}")


# exercício 1
 numero= input("Digite um número")
 if(numero>100):
    print(numero//2)

 # exercício 2 
numeroInt= input("Digite um número inteiro") 
if (numeroInt%2==0):
    print("O número é par")
else:
    print("O número é ímpar")



