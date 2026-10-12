class Campus:
    def __init__(self):
        self.nome= "Paranavaí"
        self.endereco= "Rua José Felipe Tequinha"

#Método usado ao "imprimir" um objeto
    def __str__(self):
        return f"Campus: {self.nome}"

 # Criação da classe Estudante   
class Estudante:
    def __init__(self, nome):
        self.nome=nome
        self.cpf= " "
        self.dataNasc= " "


    def __str__(self):
        return f"Estudante: {self.nome}"
    
    def apresentar(self):
        print(f"O(a) {self.nome} nasceu em {self.dataNasc}")
        if(self.cpf==""):
            print("O(a) estudante não cadastrou CPF.")
        else:
            print("CPF:", self.cpf[0:3], "...")

    

#Criação dos objetos
poliana= Estudante("Poliana Perez")
poliana.cpf="987.968.423-97"
poliana.dataNasc= "06/05/2009"
poliana.apresentar()

maju= Estudante("Maria Júlia de Jesus Barbosa")
maju.cpf="654.987.089-67"
maju.dataNasc="04/03/2009"
maju.apresentar()