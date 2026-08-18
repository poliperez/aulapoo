import arcade
import random


LARGURA = 800
ALTURA = 600
TITULO = "Coletor de Moedas"


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("Hello_Kitty.png", scale=0.1)

        self.textura_direita = arcade.load_texture("Hello_Kitty.png")
        self.textura_esquerda = arcade.load_texture("Hello_Kitty_esp.png")

    def update(self, delta_time=1 / 60):

        self.center_x += self.change_x
        self.center_y += self.change_y

        
        if self.change_x > 0:
            self.texture = self.textura_direita

        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        
        if self.left < 0:
            self.left = 0

        if self.right > LARGURA:
            self.right = LARGURA

        if self.bottom < 0:
            self.bottom = 0

        if self.top > ALTURA:
            self.top = ALTURA




class Moeda(arcade.Sprite):

    def __init__(self):
        super().__init__("MOEDA.png", scale=0.03)


class MoedaEspecial(arcade.Sprite):

    def __init__(self):
        super().__init__("MOEDA.png", scale=0.04)

        self.change_x = 150
        self.change_y = 150

    def update(self, delta_time=1 / 60):

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Rebater nas laterais
        if self.right > LARGURA:
            self.right = LARGURA
            self.change_x *= -1

        elif self.left < 0:
            self.left = 0
            self.change_x *= -1

        # Rebater em cima e embaixo
        if self.top > ALTURA:
            self.top = ALTURA
            self.change_y *= -1

        elif self.bottom < 0:
            self.bottom = 0
            self.change_y *= -1



class Inimigo(arcade.Sprite):

    def __init__(self):
        super().__init__("melody.png", scale=0.25)

        self.change_x = random.choice([-100, 100])
        self.change_y = random.choice([-100, 100])

    def update(self, delta_time=1 / 60):

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        
        if self.right > LARGURA:
            self.right = LARGURA
            self.change_x *= -1

        elif self.left < 0:
            self.left = 0
            self.change_x *= -1

        
        if self.top > ALTURA:
            self.top = ALTURA
            self.change_y *= -1

        elif self.bottom < 0:
            self.bottom = 0
            self.change_y *= -1



class InimigoEspecial(arcade.Sprite):

    def __init__(self, jogador):
        super().__init__("kuromi.png", scale=0.12)

        
        self.jogador = jogador

        
        self.velocidade = 60

    def update(self, delta_time=1 / 60):

        
        if self.center_x < self.jogador.center_x:
            self.center_x += self.velocidade * delta_time

        elif self.center_x > self.jogador.center_x:
            self.center_x -= self.velocidade * delta_time

        
        if self.center_y < self.jogador.center_y:
            self.center_y += self.velocidade * delta_time

        elif self.center_y > self.jogador.center_y:
            self.center_y -= self.velocidade * delta_time

        
        if self.left < 0:
            self.left = 0

        if self.right > LARGURA:
            self.right = LARGURA

        if self.bottom < 0:
            self.bottom = 0

        if self.top > ALTURA:
            self.top = ALTURA


class TelaInstrucoes(arcade.View):

    def __init__(self):
        super().__init__()

    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "INSTRUÇÕES",
            LARGURA // 2,
            500,
            arcade.color.PINK,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Objetivo:",
            100,
            420,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            "Colete todas as moedas espalhadas pelo mapa.",
            100,
            390,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "Teclas de Controle:",
            100,
            330,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            "↑  Mover para cima",
            120,
            295,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "↓  Mover para baixo",
            120,
            265,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "←  Mover para a esquerda",
            120,
            235,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "→  Mover para a direita",
            120,
            205,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "Moeda normal: +1 ponto",
            120,
            160,
            arcade.color.PINK,
            16
        )

        arcade.draw_text(
            "Moeda especial: +5 pontos",
            120,
            130,
            arcade.color.PINK,
            16
        )

        arcade.draw_text(
            "Inimigos: -1 ponto",
            120,
            100,
            arcade.color.PURPLE,
            16
        )

        arcade.draw_text(
            "ESC - Voltar ao menu",
            500,
            100,
            arcade.color.WHITE,
            16
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())



class TelaSobre(arcade.View):

    def __init__(self):
        super().__init__()

    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "SOBRE O JOGO",
            LARGURA // 2,
            500,
            arcade.color.PINK,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Coletor de Moedas",
            LARGURA // 2,
            430,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            "Desenvolvido por:",
            LARGURA // 2,
            350,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        # ALTERE PELO NOME DOS INTEGRANTES
        arcade.draw_text(
            "SEU NOME",
            LARGURA // 2,
            310,
            arcade.color.PINK,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC - Voltar ao menu",
            LARGURA // 2,
            100,
            arcade.color.WHITE,
            16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())



class TelaGameOver(arcade.View):

    def __init__(self, score, tempo):
        super().__init__()

        self.score = score
        self.tempo = tempo

    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "GAME OVER",
            LARGURA // 2,
            400,
            arcade.color.PURPLE,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Pontuação: {self.score}",
            LARGURA // 2,
            330,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Tempo: {self.tempo:.1f} segundos",
            LARGURA // 2,
            290,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [R] para reiniciar",
            LARGURA // 2,
            210,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [ESC] para sair",
            LARGURA // 2,
            170,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.R:
            self.window.show_view(TelaJogo())

        elif key == arcade.key.ESCAPE:
            arcade.close_window()



class TelaVitoria(arcade.View):

    def __init__(self, score, tempo):
        super().__init__()

        self.score = score
        self.tempo = tempo

    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "VOCÊ VENCEU!",
            LARGURA // 2,
            400,
            arcade.color.PINK,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Pontuação: {self.score}",
            LARGURA // 2,
            330,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Tempo: {self.tempo:.1f} segundos",
            LARGURA // 2,
            290,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [R] para jogar novamente",
            LARGURA // 2,
            210,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [ESC] para sair",
            LARGURA // 2,
            170,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.R:
            self.window.show_view(TelaJogo())

        elif key == arcade.key.ESCAPE:
            arcade.close_window()



class TelaInicial(arcade.View):

    def __init__(self):
        super().__init__()

    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "JOGO - O COLETOR DE MOEDAS",
            LARGURA // 2,
            430,
            arcade.color.PINK,
            30,
            anchor_x="center"
        )

        arcade.draw_text(
            "[J] Jogar",
            LARGURA // 2,
            330,
            arcade.color.PURPLE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[I] Instruções",
            LARGURA // 2,
            290,
            arcade.color.PURPLE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[S] Sobre o Jogo",
            LARGURA // 2,
            250,
            arcade.color.PURPLE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair",
            LARGURA // 2,
            210,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.J or key == arcade.key.ENTER:
            self.window.show_view(TelaJogo())

        elif key == arcade.key.I:
            self.window.show_view(TelaInstrucoes())

        elif key == arcade.key.S:
            self.window.show_view(TelaSobre())

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("bloco.png", scale=0.5)
        self.center_x= x
        self.center_y= y

class TelaJogo(arcade.View):

    def __init__(self):
        super().__init__()

        self.sprite_blocos= arcade.SpriteList()

        for x in range(32, LARGURA + 32, 64):
            chao= Bloco(x=x, y=30)
            self.sprite_blocos.append(chao)
        
        arcade.set_background_color(arcade.color.PINK)

        
        self.obj_list = arcade.SpriteList()
        self.moedas = arcade.SpriteList()
        self.moedas_especiais = arcade.SpriteList()
        self.inimigos = arcade.SpriteList()
        self.inimigos_especiais = arcade.SpriteList()


        self.jogador = Player()

        self.jogador.center_x = 400
        self.jogador.center_y = 300

        self.player_speed = 6

        self.score = 0

        self.tempo = 0

        

        self.alerta = ""
        self.tempo_alerta = 0

        for i in range(25):

            moeda = Moeda()

            moeda.center_x = random.randint(
                30,
                LARGURA - 30
            )

            moeda.center_y = random.randint(
                30,
                ALTURA - 30
            )

            self.moedas.append(moeda)
            self.obj_list.append(moeda)

        self.moeda_especial = MoedaEspecial()

        self.moeda_especial.center_x = 100
        self.moeda_especial.center_y = 100

        self.moedas_especiais.append(
            self.moeda_especial
        )

        self.obj_list.append(
            self.moeda_especial
        )

        self.inimigo = Inimigo()

        self.inimigo.center_x = 200
        self.inimigo.center_y = 450

        self.inimigos.append(self.inimigo)
        self.obj_list.append(self.inimigo)

        self.inimigo_especial = InimigoEspecial(
            self.jogador
        )

        self.inimigo_especial.center_x = 700
        self.inimigo_especial.center_y = 500

        self.inimigos_especiais.append(
            self.inimigo_especial
        )

        self.obj_list.append(
            self.inimigo_especial
        )

        self.engine_fisica= arcade.PhysicsEnginePlatformer(
        player_sprite=self.jogador,
        walls= self.sprite_blocos,
        gravity_constant=0.5)

        # Jogador por último
        self.obj_list.append(self.jogador)


    def on_draw(self):

        self.clear()

        self.sprite_blocos.draw()

        self.obj_list.draw()

        
        arcade.draw_text(
            f"Pontuação: {self.score}",
            10,
            ALTURA - 30,
            arcade.color.WHITE,
            16
        )

      
        arcade.draw_text(
            f"Tempo: {self.tempo:.1f}s",
            10,
            ALTURA - 55,
            arcade.color.WHITE,
            16
        )

   
        if self.tempo_alerta > 0:

            arcade.draw_text(
                self.alerta,
                LARGURA // 2,
                ALTURA - 50,
                arcade.color.PURPLE,
                22,
                anchor_x="center"
            )


    def on_update(self, delta_time):

        self.engine_fisica.update()



      
        self.obj_list.update(delta_time)

        
        if self.tempo_alerta > 0:
            self.tempo_alerta -= delta_time

        moedas_coletadas = arcade.check_for_collision_with_list(
            self.jogador,
            self.moedas
        )

        for moeda in moedas_coletadas:

            moeda.remove_from_sprite_lists()

            self.score += 1

        moedas_especiais_coletadas = (
            arcade.check_for_collision_with_list(
                self.jogador,
                self.moedas_especiais
            )
        )

        for moeda in moedas_especiais_coletadas:

            moeda.remove_from_sprite_lists()

            self.score += 5

        inimigos_colididos = arcade.check_for_collision_with_list(
            self.jogador,
            self.inimigos
        )

        for inimigo in inimigos_colididos:

            self.score -= 1

            self.alerta = "CUIDADO! -1 ponto"
            self.tempo_alerta = 1

            inimigo.center_x = random.randint(
                50,
                LARGURA - 50
            )

            inimigo.center_y = random.randint(
                50,
                ALTURA - 50
            )


        inimigos_especiais_colididos = (
            arcade.check_for_collision_with_list(
                self.jogador,
                self.inimigos_especiais
            )
        )

        for inimigo in inimigos_especiais_colididos:

            self.score -= 1

            self.alerta = "INIMIGO ESPECIAL! -1 ponto"
            self.tempo_alerta = 1

           
            inimigo.center_x = random.randint(
                50,
                LARGURA - 50
            )

            inimigo.center_y = random.randint(
                50,
                ALTURA - 50
            )

        if len(self.moedas) == 0:

            self.window.show_view(
                TelaVitoria(
                    self.score,
                    self.tempo
                )
            )

  

    def on_key_press(self, key, modifiers):

        if key == arcade.key.RIGHT:
            self.jogador.change_x = self.player_speed

        elif key == arcade.key.LEFT:
            self.jogador.change_x = -self.player_speed

        elif key == arcade.key.UP:
            self.jogador.change_y = self.player_speed

        elif key == arcade.key.DOWN:
            self.jogador.change_y = -self.player_speed

        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())

   

    def on_key_release(self, key, modifiers):

        if key in (
            arcade.key.RIGHT,
            arcade.key.LEFT
        ):
            self.jogador.change_x = 0

        if key in (
            arcade.key.UP,
            arcade.key.DOWN
        ):
            self.jogador.change_y = 0


def executar():

    janela = arcade.Window(
        LARGURA,
        ALTURA,
        TITULO
    )

    tela_inicial = TelaInicial()

    janela.show_view(tela_inicial)

    arcade.run()



if __name__ == "__main__":
    executar()

