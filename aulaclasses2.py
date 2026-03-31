class ContaBancaria:
    def __init__(self, numero, titular, saldo):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo
        
    def depositar(self, valor):
        self.saldo += valor
        print("Depósito realizado")

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente")
            print(f"Saldo atual de {self.titular}: R$ {self.saldo}")
        else:
            self.saldo -= valor
            print("Saque realizado com sucesso")
            print(f"Novo saldo de {self.titular}: R$ {self.saldo}")

    def transferir(self, valor, conta_transferencia):
        if valor > self.saldo:
            print("Saldo insuficiente para transferir")
        else:
            self.saldo -= valor
            conta_transferencia.saldo += valor
            print("Transferência realizada")
            print(f"Saldo de {self.titular}: R$ {self.saldo}")
            print(f"Saldo de {conta_transferencia.titular}: R$ {conta_transferencia.saldo}")



poliana = ContaBancaria(6, "Poliana", 3000)
maju = ContaBancaria(4, "Maria Júlia", 2000)

print("Saldo inicial:")
print(f"Saldo inicial de {poliana.titular}: R$ {poliana.saldo}")
print(f"Saldo inicial de {maju.titular}: R$ {maju.saldo}")


poliana.depositar(200)
maju.sacar(1000)
poliana.transferir(1200, maju)
maju.sacar(300)

print("Saldo final:")
print(f"Saldo final de {poliana.titular}: R$ {poliana.saldo}")
print(f"Saldo final de {maju.titular}: R$ {maju.saldo}")