class Animal: 
    def __init__(self,nome,especie,patas):
        self.nome =nome
        self.especie =especie
        self.patas =patas
    
    
    def respirar(self):
        print("Respirando...")
        
    def rugir(self):
        print("Rugindo...")
        
        
class Cachorro(Animal):
    def abanar_rabo(self):
        print("Abanando o rabo")
        
    def rugir(Animal):
        print("Au Au!")
        
        
class Gato(Animal):
    def ronronar(self):
        print("Ronronando")
        
    def rugir(Animal):
        print("Miau!")
