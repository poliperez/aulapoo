import arcade

# Configurações da janela
LARGURA = 800
ALTURA = 600
TITULO = "Coletor de Moedas"
GRAVIDADE = 0.5


class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
       super().__init__(scale=0.5)
       self.center_x = x
       self.center_y = y

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Hello_Kitty.png", scale=0.3)

        # Texturas para esquerda e direita
        self.textura_direita = arcade.load_texture("Hello_Kitty.png")
        self.textura_esquerda = arcade.load_texture("Hello_Kitty.png")

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
        super().__init__("MOEDA.png", scale=0.5)

    def update(self, delta_time=1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x > LARGURA:
            self.change_x = 0
        elif self.center_x < 0:
            self.change_x = 0

        if self.center_y > ALTURA:
            self.change_y = 0
        elif self.center_y < 0:
            self.change_y = 0

        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self.personagem,
            walls=self.sprite_blocos>
            gravity_constant= GRAVIDADE

         )

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


class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.velocidade = 4

        self.obj_list = arcade.SpriteList()

        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 300

        self.obj_list.append(self.jogador)

    def on_draw(self):
        self.clear()
        self.obj_list.draw()

    def on_update(self, delta_time):
        self.engine_fisica.update()
        self.obj_list.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.jogador.change_x = self.velocidade

        elif key == arcade.key.LEFT:
            self.jogador.change_x = -self.velocidade

        elif key == arcade.key.UP:
            self.jogador.change_y = self.velocidade

        elif key == arcade.key.DOWN:
            self.jogador.change_y = -self.velocidade

        elif key == arcade.key.ESCAPE:
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