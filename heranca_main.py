from aula1205 import Animal, Gato, Cachorro
mello = Gato("Mello", "gato", 4)

print(f"meu gato é o {mello.nome}")
mello.respirar()
mello.ronronar()
mello.rugir()

floki=Cachorro("Floki", "cachorro", 4)

print(f"meu cachorro é o {floki.nome}")

floki.abanar_rabo()
floki.respirar()
floki.rugir()