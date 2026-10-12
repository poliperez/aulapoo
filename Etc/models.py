from peewee import *
import datetime

conexao = SqliteDatabase("meu_banco.db")

class Contato(Model):
    
    nome = CharField()
    telefone = CharField()
    
    def __str__(self):
        return f"{self.nome}: {self.telefone}"
    
    class Meta:
        database = conexao

    conexao.connect()
    conexao.create_tables([Contato])