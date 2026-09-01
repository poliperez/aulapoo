import arcade
import random
import os

LARGURA = 800
ALTURA = 600
TITULO = "Coletor de Moedas"


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "Hello_Kitty.png",
            scale=0.1
        )

        self.textura_direita = arcade.load_texture(
            "Hello_Kitty.png"
        )

        self.textura_esquerda = arcade.load_texture(
            "Hello_Kitty_esp.png"
        )

    def update(self, delta_time):
        if self.change_x > 0:
            self.texture = self.textura_direita

        elif self.change_x < 0:
            self.texture = self.textura_esquerda
            
            
    def state_machine(self):
        
        
        
        if self.change_y != 0:
            self.jump()
            return
        
        if self.change_x == 0:
            self.idle()
            return
        
        #change y == 0 e change x != 0
        self.walk()
    
    def walk(self):
        pass
    def jump(self):
        pass
    def idle(self):
        pass


class Moeda(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "MOEDA.png",
            scale=0.02
        )


class MoedaEspecial(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "MOEDA.png",
            scale=0.03
        )

        self.change_x = 150
        self.change_y = 100

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        if self.right >= LARGURA:
            self.right = LARGURA
            self.change_x *= -1

        elif self.left <= 0:
            self.left = 0
            self.change_x *= -1

        if self.top >= ALTURA:
            self.top = ALTURA
            self.change_y *= -1

        elif self.bottom <= 0:
            self.bottom = 0
            self.change_y *= -1


class Inimigo(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "kuromi.png",
            scale=0.3
        )

        self.change_x = 150

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time

        if self.right >= LARGURA:
            self.right = LARGURA
            self.change_x *= -1

        elif self.left <= 0:
            self.left = 0
            self.change_x *= -1


class InimigoEspecial(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "melody.png",
            scale=0.25
        )

        self.velocidade = 100
        self.change_x = 0

    def perseguir_jogador(self, jogador):
        if jogador.center_x > self.center_x:
            self.change_x = self.velocidade

        elif jogador.center_x < self.center_x:
            self.change_x = -self.velocidade

        else:
            self.change_x = 0


class Bloco(arcade.Sprite):

    def __init__(self, escala=0.35):
        super().__init__(
            "bloco.png",
            scale=escala
        )


class TelaJogo(arcade.View):

    def __init__(self):
        super().__init__()

        arcade.set_background_color(
            arcade.color.PINK
        )

        self.pontuacao = 0
        self.tempo = 0
        self.sofreu_dano = False
        self.alerta = ""
        self.tempo_alerta = 0
        self.tempo_invulnerabilidade = 0

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_moeda_especial = arcade.SpriteList()
        self.sprite_blocos = arcade.SpriteList()
        self.sprite_inimigos = arcade.SpriteList()
        self.sprite_inimigos_especiais = arcade.SpriteList()

        self.jogador = Player()

        self.jogador.center_x = 400
        self.jogador.center_y = 100

        self.sprite_jogador.append(
            self.jogador
        )

        for x in range(80, LARGURA, 160):
            bloco = Bloco(
                escala=0.35
            )

            bloco.center_x = x
            bloco.center_y = 25

            self.sprite_blocos.append(
                bloco
            )

        plataformas = [
            (120, 250),
            (330, 220),
            (550, 320),
            (700, 240)
        ]

        for x, y in plataformas:
            bloco = Bloco(
                escala=0.28
            )

            bloco.center_x = x
            bloco.center_y = y

            self.sprite_blocos.append(
                bloco
            )

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.jogador,
            platforms=self.sprite_blocos,
            gravity_constant=1
        )

        posicoes_moedas = [
            (100, 110),
            (300, 110),
            (500, 110),
            (700, 110),
            (120, 300),
            (330, 270),
            (550, 360),
            (700, 290),
            (250, 390),
            (550, 430),
        ]

        for x, y in posicoes_moedas:
            moeda = Moeda()

            moeda.center_x = x
            moeda.center_y = y

            self.sprite_moedas.append(
                moeda
            )

        self.moeda_especial = MoedaEspecial()

        self.moeda_especial.center_x = 650
        self.moeda_especial.center_y = 500

        self.sprite_moeda_especial.append(
            self.moeda_especial
        )

        inimigo = Inimigo()

        inimigo.center_x = 200
        inimigo.center_y = 100

        self.sprite_inimigos.append(
            inimigo
        )

        self.inimigo_especial = InimigoEspecial()

        self.inimigo_especial.center_x = 600
        self.inimigo_especial.center_y = 100

        self.sprite_inimigos_especiais.append(
            self.inimigo_especial
        )

        self.physics_engine_inimigo_especial = (
            arcade.PhysicsEnginePlatformer(
                self.inimigo_especial,
                platforms=self.sprite_blocos,
                gravity_constant=1
            )
        )

    def on_draw(self):
        self.clear()

        self.sprite_jogador.draw()
        self.sprite_moedas.draw()
        self.sprite_moeda_especial.draw()
        self.sprite_blocos.draw()
        self.sprite_inimigos.draw()
        self.sprite_inimigos_especiais.draw()

        arcade.draw_text(
            f"Moedas Coletadas: {self.pontuacao}",
            10,
            570,
            arcade.color.WHITE,
            14
        )

        arcade.draw_text(
            f"Tempo: {self.tempo:.1f}s",
            650,
            570,
            arcade.color.WHITE,
            14
        )

        if self.alerta:
            arcade.draw_text(
                self.alerta,
                LARGURA / 2,
                520,
                arcade.color.RED,
                22,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        self.tempo += delta_time

        self.sprite_jogador.update(
            delta_time
        )

        self.physics_engine.update()

        if self.jogador.left < 0:
            self.jogador.left = 0

        if self.jogador.right > LARGURA:
            self.jogador.right = LARGURA

        if self.jogador.top > ALTURA:
            self.jogador.top = ALTURA

        if self.jogador.bottom < 0:
            self.jogador.bottom = 0
            self.jogador.change_y = 0

        self.sprite_moeda_especial.update(
            delta_time
        )

        self.sprite_inimigos.update(
            delta_time
        )

        self.inimigo_especial.perseguir_jogador(
            self.jogador
        )

        self.physics_engine_inimigo_especial.update()

        if self.tempo_invulnerabilidade > 0:
            self.tempo_invulnerabilidade -= delta_time

        if self.tempo_alerta > 0:
            self.tempo_alerta -= delta_time

        else:
            self.alerta = ""

        moedas_colididas = (
            arcade.check_for_collision_with_list(
                self.jogador,
                self.sprite_moedas
            )
        )

        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
            self.pontuacao += 1

        moedas_especiais_colididas = (
            arcade.check_for_collision_with_list(
                self.jogador,
                self.sprite_moeda_especial
            )
        )

        for moeda in moedas_especiais_colididas:
            moeda.remove_from_sprite_lists()
            self.pontuacao += 5

        if self.tempo_invulnerabilidade <= 0:

            inimigos_colididos = (
                arcade.check_for_collision_with_list(
                    self.jogador,
                    self.sprite_inimigos
                )
            )

            for inimigo in inimigos_colididos:
                self.pontuacao -= 1
                self.sofreu_dano = True

                self.alerta = (
                    "CUIDADO! Você foi atingido!"
                )

                self.tempo_alerta = 2
                self.tempo_invulnerabilidade = 1.5

                if (
                    self.jogador.center_x
                    < inimigo.center_x
                ):
                    self.jogador.change_x = -8

                else:
                    self.jogador.change_x = 8

        inimigos_especiais_colididos = (
            arcade.check_for_collision_with_list(
                self.jogador,
                self.sprite_inimigos_especiais
            )
        )

        if (
            inimigos_especiais_colididos
            and self.tempo_invulnerabilidade <= 0
        ):

            for inimigo in inimigos_especiais_colididos:
                self.pontuacao -= 1
                self.sofreu_dano = True

                self.alerta = (
                    "CUIDADO! O inimigo especial te encontrou!"
                )

                self.tempo_alerta = 2
                self.tempo_invulnerabilidade = 1.5

                nova_posicao_encontrada = False

                while not nova_posicao_encontrada:
                    novo_x = random.randint(
                        50,
                        750
                    )

                    novo_y = 100

                    distancia = abs(
                        novo_x
                        - self.jogador.center_x
                    )

                    if distancia > 150:
                        nova_posicao_encontrada = True

                        inimigo.center_x = novo_x
                        inimigo.center_y = novo_y

                inimigo.change_x = 0

        if len(self.sprite_moedas) == 0:

            tela_game_over = TelaGameOver(
                self.pontuacao,
                self.tempo,
                self.sofreu_dano
            )

            self.window.show_view(
                tela_game_over
            )

    def on_key_press(self, key, modifiers):

        if (
            key == arcade.key.RIGHT
            or key == arcade.key.D
        ):
            self.jogador.change_x = 5

        elif (
            key == arcade.key.LEFT
            or key == arcade.key.A
        ):
            self.jogador.change_x = -5

        elif (
            key == arcade.key.UP
            or key == arcade.key.W
        ):
            if self.physics_engine.can_jump():
                self.jogador.change_y = 15

        elif key == arcade.key.ESCAPE:
            self.window.show_view(
                TelaInicial()
            )

    def on_key_release(self, key, modifiers):

        if (
            key == arcade.key.RIGHT
            or key == arcade.key.D
        ):
            self.jogador.change_x = 0

        elif (
            key == arcade.key.LEFT
            or key == arcade.key.A
        ):
            self.jogador.change_x = 0


class TelaSobre(arcade.View):

    def __init__(self):
        super().__init__()

        self.sprite_avatares = arcade.SpriteList()

        if os.path.exists("melody.png"):

            avatar1 = arcade.Sprite(
                "melody.png",
                scale=0.15
            )

            avatar1.center_x = 400
            avatar1.center_y = 200

            self.sprite_avatares.append(
                avatar1
            )

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "SOBRE O JOGO",
            LARGURA // 2,
            500,
            arcade.color.PURPLE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Objetivo:",
            LARGURA // 2,
            420,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "Coletar todas as moedas espalhadas pelo mapa.",
            LARGURA // 2,
            385,
            arcade.color.PINK,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            "Desenvolvido por:",
            LARGURA // 2,
            320,
            arcade.color.PURPLE,
            20,
            anchor_x="center"
        )

        self.sprite_avatares.draw()

        arcade.draw_text(
            "POLIANA",
            LARGURA // 2,
            90,
            arcade.color.PINK,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] ou [M] Voltar ao menu",
            LARGURA // 2,
            20,
            arcade.color.PINK,
            15,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if (
            key == arcade.key.ESCAPE
            or key == arcade.key.M
        ):
            self.window.show_view(
                TelaInicial()
            )


class TelaInstrucoes(arcade.View):

    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "INSTRUÇÕES",
            LARGURA / 2,
            480,
            arcade.color.PURPLE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Objetivo: coletar todas as moedas espalhadas pelo mapa.",
            LARGURA / 2,
            410,
            arcade.color.PINK,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "A / ← : mover para a esquerda",
            LARGURA / 2,
            350,
            arcade.color.PINK,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "D / → : mover para a direita",
            LARGURA / 2,
            315,
            arcade.color.PINK,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "W / ↑ : pular",
            LARGURA / 2,
            280,
            arcade.color.PINK,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Moeda normal: +1 ponto",
            LARGURA / 2,
            225,
            arcade.color.PURPLE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Moeda especial: +5 pontos",
            LARGURA / 2,
            190,
            arcade.color.PURPLE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "CUIDADO: os inimigos retiram 1 ponto!",
            LARGURA / 2,
            155,
            arcade.color.RED,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "O inimigo especial persegue você pelo chão.",
            LARGURA / 2,
            120,
            arcade.color.RED,
            15,
            anchor_x="center"
        )

        arcade.draw_text(
            "Após atingir você, ele se teletransporta.",
            LARGURA / 2,
            95,
            arcade.color.RED,
            15,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] ou [M] : voltar ao Menu Principal",
            LARGURA / 2,
            55,
            arcade.color.PINK,
            17,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if (
            key == arcade.key.ESCAPE
            or key == arcade.key.M
        ):
            self.window.show_view(
                TelaInicial()
            )


class TelaGameOver(arcade.View):

    def __init__(
        self,
        pontuacao,
        tempo,
        sofreu_dano
    ):
        super().__init__()

        self.pontuacao = pontuacao
        self.tempo = tempo
        self.sofreu_dano = sofreu_dano

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "FIM DE JOGO!",
            LARGURA / 2,
            420,
            arcade.color.PURPLE,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Pontuação final: {self.pontuacao}",
            LARGURA / 2,
            340,
            arcade.color.PINK,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Tempo total: {self.tempo:.1f} segundos",
            LARGURA / 2,
            290,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

        if not self.sofreu_dano:

            arcade.draw_text(
                "PARABÉNS! Você escapou de todos os inimigos perfeitamente!",
                LARGURA / 2,
                220,
                arcade.color.GREEN,
                18,
                anchor_x="center"
            )

        else:

            arcade.draw_text(
                "Parabéns por terminar o jogo!",
                LARGURA / 2,
                220,
                arcade.color.PURPLE,
                18,
                anchor_x="center"
            )

        arcade.draw_text(
            "[M] Voltar ao Menu Principal",
            LARGURA / 2,
            140,
            arcade.color.PINK,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair do Jogo",
            LARGURA / 2,
            90,
            arcade.color.PINK,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.M:
            self.window.show_view(
                TelaInicial()
            )

        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class TelaInicial(arcade.View):

    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "COLETOR DE MOEDAS",
            LARGURA / 2,
            420,
            arcade.color.PURPLE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "[J] Jogar",
            LARGURA / 2,
            320,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[I] Instruções",
            LARGURA / 2,
            270,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[S] Sobre o Jogo",
            LARGURA / 2,
            220,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair",
            LARGURA / 2,
            170,
            arcade.color.PINK,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.J:

            tela_jogo = TelaJogo()

            self.window.show_view(
                tela_jogo
            )

        elif key == arcade.key.I:

            tela_instrucoes = TelaInstrucoes()

            self.window.show_view(
                tela_instrucoes
            )

        elif key == arcade.key.S:

            tela_sobre = TelaSobre()

            self.window.show_view(
                tela_sobre
            )

        elif key == arcade.key.ESCAPE:
            arcade.close_window()


def executar():

    janela = arcade.Window(
        LARGURA,
        ALTURA,
        TITULO
    )

    tela_inicial = TelaInicial()

    janela.show_view(
        tela_inicial
    )

    arcade.run()


if __name__ == "__main__":
    executar()