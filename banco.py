import datetime                 
from peewee import SqliteDatabase, Model, CharField, IntegerField, FloatField, DateTimeField
       

db = SqliteDatabase("ranking.db")


class BaseModel(Model):
    class Meta:
        database = db


class Pontuacao(BaseModel):
    nome_jogador = CharField()                   
    pontos = IntegerField()                      
    tempo_partida = FloatField()                
   
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.nome_jogador} - {self.pontos} pts ({self.tempo_partida:.1f}s)"


def inicializar_banco():
    db.connect(reuse_if_open=True)   
    db.create_tables([Pontuacao])   

def buscar_top10():
   
    consulta = (Pontuacao
                .select()
                .order_by(Pontuacao.pontos.desc(), Pontuacao.tempo_partida.asc())
                .limit(10))
    
    return list(consulta)

inicializar_banco()