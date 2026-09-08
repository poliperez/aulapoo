from peewee import *
import datetime

db = SqliteDatabase('ranking.db')

class BaseModel(Model):
    class Meta:
        database = db


class Pontuacao(BaseModel):
    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    data_hora = DateTimeField(
        default=datetime.datetime.now)

    def __str__(self):
        return (f"{self.nome_jogador} - "
                f"{self.pontos} pts "
                f"({self.tempo_partida:.1f}s)")
