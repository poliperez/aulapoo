# class Aluno:
#         def __init__(self, nome, idade, curso, notas):
#                 self.nome= nome
#                 self.idade=idade
#                 self.curso=curso
#                 self.notas= notas

#         def calcular_media(self):
#                soma= 0.0
#                for i in range(0, len(self.notas)):
#                       soma+= self.notas[i]
                      
#                media = soma/len(self.notas)
#                return media
               


#         def apresentar(self):
#             print(f"Olá, meu nome é {self.nome}, tenho {self.idade} anos e faço curso de {self.curso}")

# print("Informe os dados: ")
# nome=str(input("Nome:"))
# idade= int(input("Idade:"))
# curso= str(input("Curso:"))

# aluno1= Aluno(nome, idade, curso, notas)
# aluno1.apresentar(nome, idade, curso, [7,8,10])

# print("Informe as notas: ")
# nota1=input("Nota 1:")
# nota2=input("Nota 2:")
# nota3=input("Nota 3:")


# print(f"A Média das notas é {aluno1.media()}")


class Livro:
    def __init__ (self, titulo):
        self.titulo= titulo
        self.disponivel= True

    def emprestar(self):
        if self.disponivel==True:
            self.disponivel==False
            print("Livro emprestado com sucesso")

        else:
            print("O livro já está emprestado")

    def devolver(self):
        self.disponivel=True
        print("Livro devolvido com sucesso")


livro1= Livro("Metamorfose")

livro1.emprestar()
livro1.emprestar()
livro1.devolver()
