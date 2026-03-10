import os
print("Configurando email")
comando_email= "git config user.email \"polianaperez31@gmail.com\" "
os.system(comando_email)

print("Adicionando modificações")
comando1= "git add *"
os.system(comando1)

mensagem= input("Mensagem do commit: ")

while(len(mensagem) < 5):
    print("Mensagem muito pequena, detalhe mais")
    mensagem = input("Mensagem do commit: ")

print("Registrando alterações")
comando2= "git commit -m '" + mensagem + "'"
os.system(comando2)

print("Enviando projeto ao github")
comando3= "git push"
os.system(comando3)
