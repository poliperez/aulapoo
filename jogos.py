import arcade #Rodar   py -3.13 .\jogos.py
import random

# Configurações da janela
LARGURA = 800
ALTURA = 600
TITULO = "Coletor de Moedas"


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Hello_Kitty.png", scale=0.1)

        # Texturas para esquerda e direita
        self.textura_direita = arcade.load_texture("Hello_Kitty.png")
        self.textura_esquerda = arcade.load_texture("Hello_Kitty_esp.png")

    def update(self, delta_time=1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        # Limites da tela
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
    def __init__(self, special : bool =False):
        super().__init__("MOEDA.png", scale=0.03)
        self.change_x = 100
        self.change_y = 100
        self.special = special

    def update(self, delta_time=1 / 60):
        if not self.special:
            return

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
       
        if self.right > LARGURA:
            self.change_x *= -1
        elif self.left < 0:
            self.change_x *= -1

        if self.top > ALTURA:
            self.change_y *= -1
        elif self.bottom < 0:
            self.change_y *= -1

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("MOEDA.png", scale=0.04)

        # Velocidade horizontal e vertical
        self.change_x = 100
        self.change_y = 100

    def update(self, delta_time=1 / 60):

        # Movimento
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Rebater na esquerda e direita
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


class TelaSobre(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

        arcade.draw_text( "SOBRE O JOGO", LARGURA // 2,500,arcade.color.GOLD, 32,anchor_x="center"
        )

        arcade.draw_text("Objetivo:",100,420, arcade.color.WHITE,20
        )

        arcade.draw_text("Coletar todas as moedas espalhadas pelo mapa.",100,390,arcade.color.WHITE,16
        )

        arcade.draw_text("Teclas de Controle:",100,320,arcade.color.WHITE,20
        )

        arcade.draw_text( "↑  Mover para cima",120,285, arcade.color.WHITE,16
        )

        arcade.draw_text("↓  Mover para baixo",120, 255, arcade.color.WHITE,16
        )

        arcade.draw_text("←  Mover para a esquerda", 120,225,arcade.color.WHITE,16
        )

        arcade.draw_text("→  Mover para a direita", 120,195, arcade.color.WHITE,16
        )

        arcade.draw_text("ESC  Voltar ao menu inicial", 120, 165, arcade.color.WHITE, 16
        )

        arcade.draw_text("Desenvolvido por: SEU NOME", 100,  100, arcade.color.PINK, 18
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)


class TelaVitoria(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

        arcade.draw_text( "VOCÊ VENCEU!", LARGURA // 2, 350, arcade.color.SILVER, 40, anchor_x="center"
        )

        arcade.draw_text("Pressione ESC para sair", LARGURA // 2, 250, arcade.color.PINK, 20, anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()


class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "Jogo - O Coletor de Moedas",
            LARGURA // 2,
            400,
            arcade.color.PINK,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [J] para Jogar",
            LARGURA // 2,
            300,
            arcade.color.PURPLE,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [ESC] para Tela de Vitória",
            LARGURA // 2,
            240,
            arcade.color.PURPLE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J or key == arcade.key.ENTER:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)

        elif key == arcade.key.ESCAPE:
            tela_vitoria = TelaVitoria()
            self.window.show_view(tela_vitoria)

        elif key == arcade.key.I:
            tela_inst = TelaSobre()
            self.window.show_view(tela_inst)


class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.velocidade = 4

        self.obj_list = arcade.SpriteList()

        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 300

        self.moeda = Moeda(True)

        self.moeda.center_x = 100
        self.moeda.center_y = 100

        for i in range(25):


        self.obj_list.append(self.moeda)
        self.obj_list.append(self.jogador)

    def on_draw(self):
        self.clear()
        self.obj_list.draw()

    def on_update(self, delta_time):
        self.obj_list.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.jogador.change_x = self.velocidade

        if key == arcade.key.LEFT:
            self.jogador.change_x = -self.velocidade

        if key == arcade.key.UP:
            self.jogador.change_y = self.velocidade

        if key == arcade.key.DOWN:
            self.jogador.change_y = -self.velocidade

        if key == arcade.key.ESCAPE:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.jogador.change_x = 0

        if key in (arcade.key.UP, arcade.key.DOWN):
            self.jogador.change_y = 0


def executar():
    janela = arcade.Window(LARGURA, ALTURA, TITULO)

    tela_inicial = TelaInicial()
    janela.show_view(tela_inicial)

    arcade.run()


if __name__ == "__main__":
    executar()








class InimigoEspecial(arcade.Sprite):
    def __init__(self, jogador):
        super().__init__("Hello_Kitty.png", scale=0.08)

        # Guarda uma referência ao jogador
        self.jogador = jogador

        # Velocidade do inimigo especial
        self.velocidade = 60

    def update(self, delta_time=1 / 60):

        # Persegue o jogador horizontalmente
        if self.center_x < self.jogador.center_x:
            self.center_x += self.velocidade * delta_time

        elif self.center_x > self.jogador.center_x:
            self.center_x -= self.velocidade * delta_time

        # Persegue o jogador verticalmente
        if self.center_y < self.jogador.center_y:
            self.center_y += self.velocidade * delta_time

        elif self.center_y > self.jogador.center_y:
            self.center_y -= self.velocidade * delta_time

        # Mantém o inimigo dentro da tela
        if self.left < 0:
            self.left = 0

        if self.right > LARGURA:
            self.right = LARGURA

        if self.bottom < 0:
            self.bottom = 0

        if self.top > ALTURA:
            self.top = ALTURA


# ============================================================
# TELA SOBRE
# ============================================================

class TelaSobre(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "SOBRE O JOGO",
            LARGURA // 2,
            500,
            arcade.color.GOLD,
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
            "Coletar todas as moedas espalhadas pelo mapa.",
            100,
            390,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "Teclas de Controle:",
            100,
            320,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            "↑  Mover para cima",
            120,
            285,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "↓  Mover para baixo",
            120,
            255,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "←  Mover para a esquerda",
            120,
            225,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "→  Mover para a direita",
            120,
            195,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "ESC  Voltar ao menu inicial",
            120,
            165,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            "Desenvolvido por: SEU NOME",
            100,
            100,
            arcade.color.PINK,
            18
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)


# Códigos que o Chat me passou qe segundo ele estão corretos, nas classes que tem os inimigos
# tem que trocar a imagem da Hello kitty pela Kuromi, no código acima eu deixei duas classes de moeda
# especial, pois não sei qual delas vai funcionar.

class TelaVitoria(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "VOCÊ VENCEU!",
            LARGURA // 2,
            350,
            arcade.color.SILVER,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione ESC para sair",
            LARGURA // 2,
            250,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()


# ============================================================
# TELA INICIAL
# ============================================================

class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "Jogo - O Coletor de Moedas",
            LARGURA // 2,
            400,
            arcade.color.PINK,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [J] para Jogar",
            LARGURA // 2,
            300,
            arcade.color.PURPLE,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [ESC] para Tela de Vitória",
            LARGURA // 2,
            240,
            arcade.color.PURPLE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.J or key == arcade.key.ENTER:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)

        elif key == arcade.key.ESCAPE:
            tela_vitoria = TelaVitoria()
            self.window.show_view(tela_vitoria)

        elif key == arcade.key.I:
            tela_inst = TelaSobre()
            self.window.show_view(tela_inst)


# ============================================================
# TELA DO JOGO
# ============================================================

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.velocidade = 4

        # Lista geral de objetos
        self.obj_list = arcade.SpriteList()

        # ----------------------------------------------------
        # JOGADOR
        # ----------------------------------------------------

        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 300

        # ----------------------------------------------------
        # MOEDA NORMAL
        # ----------------------------------------------------

        self.moeda = Moeda()
        self.moeda.center_x = 100
        self.moeda.center_y = 100

        # ----------------------------------------------------
        # MOEDA ESPECIAL
        # ----------------------------------------------------

        self.moeda_especial = MoedaEspecial()
        self.moeda_especial.center_x = 600
        self.moeda_especial.center_y = 400

        # ----------------------------------------------------
        # INIMIGO COMUM
        # ----------------------------------------------------

        self.inimigo = Inimigo()
        self.inimigo.center_x = 200
        self.inimigo.center_y = 450

        # ----------------------------------------------------
        # INIMIGO ESPECIAL
        # ----------------------------------------------------

        self.inimigo_especial = InimigoEspecial(self.jogador)
        self.inimigo_especial.center_x = 700
        self.inimigo_especial.center_y = 500

        # ----------------------------------------------------
        # ADICIONANDO OS OBJETOS À LISTA
        # ----------------------------------------------------

        self.obj_list.append(self.moeda)
        self.obj_list.append(self.moeda_especial)
        self.obj_list.append(self.inimigo)
        self.obj_list.append(self.inimigo_especial)
        self.obj_list.append(self.jogador)

    def on_draw(self):
        self.clear()

        # Desenha todos os objetos
        self.obj_list.draw()

    def on_update(self, delta_time):

        # Atualiza todos os objetos
        self.obj_list.update(delta_time)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.RIGHT:
            self.jogador.change_x = self.velocidade

        if key == arcade.key.LEFT:
            self.jogador.change_x = -self.velocidade

        if key == arcade.key.UP:
            self.jogador.change_y = self.velocidade

        if key == arcade.key.DOWN:
            self.jogador.change_y = -self.velocidade

        if key == arcade.key.ESCAPE:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)

    def on_key_release(self, key, modifiers):

        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.jogador.change_x = 0

        if key in (arcade.key.UP, arcade.key.DOWN):
            self.jogador.change_y = 0


# ============================================================
# EXECUTAR O JOGO
# ============================================================

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