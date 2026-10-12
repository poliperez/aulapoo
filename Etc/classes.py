class Jogador:
    def__init__(self, nome, nickname, turma):
        self.nome= nome
        self.nickname= nickname
        self.turma= turma
        
    def mostrar_dados(self):
        return f"{self.nome} ({self.nickname}) - {self.turma}"
        
class Equipe: 
    def__init__(self, nome, jogodisputa):
        self.nome= nome
        self.jogodisputa= jogodisputa
        self.jogadores= []
    
    def adicionar_jogadores(self, jogador):
        self.jogadores += [jogador]

    def listar_jogadores(self):
        if (len(self.jogadores)==0):
            print("Nenhum jogador na equipe")
        else:
            for i in self.jogadores:
                print(i.mostrar_dados())

    def mostrar_dados(self):
        return f"{self.nome} ({self.jogodisputa}) - {len(self.jogadores)} jogadores"