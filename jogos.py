import arcade #Rodar  py -3.13 .\jogos.py 
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


class MoedaEspecial(arcade.Sprite):
    def __init__(self, special : bool =False):
        super().__init__("MOEDA.png", scale=0.03)
        self.change_x = 150
        self.change_y = 150
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

class InimigoEspecial(arcade.Sprite):
    def __init__(self, jogador):
        super().__init__("kuromi.png", scale=0.15)

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


class TelaGameOver(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "GAME OVER",
            LARGURA // 2,
            350,
            arcade.color.RED,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione ESC para sair",
            LARGURA // 2,
            250,
            arcade.color.RED,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [R] para reiniciar",
            LARGURA // 2,
            200,
            arcade.color.GREEN,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.R:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.PINK)

        self.obj_list = arcade.SpriteList()

        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 300
        self.player_speed = 6

        self.inimigo_especial = InimigoEspecial(self.jogador)
        self.obj_list.append(self.inimigo_especial)

        self.moeda = MoedaEspecial(True)

        self.moeda.center_x = 100
        self.moeda.center_y = 100

        self.obj_list.append(self.moeda)


        for i in range(25):
            moeda = MoedaEspecial()
            moeda.center_x = random.randint(20, LARGURA - 20)
            moeda.center_y = random.randint(20, ALTURA - 20)
            self.obj_list.append(moeda)

        self.obj_list.append(self.jogador)
        self.score = 0

    def on_draw(self):
        self.clear()
        self.obj_list.draw()

        draw_text = f"Pontuação: {self.score}"  # Subtrai o jogador e o inimigo especial
        arcade.draw_text(draw_text, 10, ALTURA - 30, arcade.color.WHITE, 16)

    def on_update(self, delta_time):
        self.obj_list.update(delta_time)

        if (arcade.check_for_collision(self.jogador, self.inimigo_especial)):
            tela_game_over = TelaGameOver()
            self.window.show_view(tela_game_over)

        if self.score == 25:
            tela_vitoria = TelaVitoria()
            self.window.show_view(tela_vitoria)

        moedas_coletadas = arcade.check_for_collision_with_list(self.jogador, self.obj_list)
        for moeda in moedas_coletadas:
            if isinstance(moeda, MoedaEspecial):
                moeda.remove_from_sprite_lists()
                self.score += 1


    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.jogador.change_x = self.player_speed

        if key == arcade.key.LEFT:
            self.jogador.change_x = -self.player_speed

        if key == arcade.key.UP:
            self.jogador.change_y = self.player_speed

        if key == arcade.key.DOWN:
            self.jogador.change_y = -self.player_speed

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