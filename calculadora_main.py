from heranca_exercicios import *
calculadora01= Calculadora("Daten", "20.4", 2009)

valor1= int(input("Digite o valor 1"))
valor2= int(input("Digite o valor 2"))

calculadora01.somar(valor1, valor2)

calculadora01.subtrair(valor1, valor2)

calculadora01.multiplicar(valor1, valor2)

calculadora01.dividir(valor1, valor2)

calculadora02= CalculadoraCientifica("Daten", "28.7", 2018)

valor03= float(input("Digite um valor"))

calculadora02.potencia(valor03, 3)

calculadora02.raiz_quadrada(valor03)