import arcade
import random
import os
from banco import *

ASSETS_DIR = os.path.join(
	os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	"Assets"
)

LARGURA = 1800
ALTURA = 800
TITULO = "Coletor de Moedas"

class Player(arcade.Sprite):
    def __init__(self):
        self.spr_idle = os.path.join(ASSETS_DIR, "hk_idle.png")
        self.spr_idle_r = os.path.join(ASSETS_DIR, "hk_idle_r.png")
        self.spr_jump = os.path.join(ASSETS_DIR, "hk_jump.png")
        self.spr_jump_r = os.path.join(ASSETS_DIR, "hk_jump_r.png")

        super().__init__(
            self.spr_idle,
            scale=0.1
        )

        textura = arcade.load_texture(os.path.join(ASSETS_DIR, "Hello_Kitty_spritesheat.png"))

        largura_sprite = textura.width // 4
        altura_sprite = textura.height

        sheet_direita = arcade.load_spritesheet(
            os.path.join(ASSETS_DIR, "Hello_Kitty_spritesheat.png")
        )

        self.passos_direita = sheet_direita.get_texture_grid(
            size=(
                largura_sprite,
                altura_sprite
            ),
            columns=3,
            count=3
        )

        self.passos_esquerda = []

        for frame in self.passos_direita:
            self.passos_esquerda.append(
                frame.flip_left_right()
            )

        self.textura_parado_d = arcade.load_texture(
            self.spr_idle
        )

        self.textura_parado_e = arcade.load_texture(
            self.spr_idle_r
        )

        self.textura_pulo_d = arcade.load_texture(
            self.spr_jump
        )

        self.textura_pulo_e = arcade.load_texture(
            self.spr_jump_r
        )

        self.virado_para = "DIREITA"

        self.quadro_atual = 0

        self.tempo_animacao = 0.0

    def update(self, delta_time: float = 1 / 60):
        if self.change_x > 0:
            self.virado_para = "DIREITA"

        elif self.change_x < 0:
            self.virado_para = "ESQUERDA"

        self.state_machine(delta_time)

    def state_machine(self, delta_time):
        if self.change_y != 0:
            self.jump()
            return

        if self.change_x == 0:
            self.idle()
            return

        self.walk(delta_time)

    def walk(self, delta_time):

        self.tempo_animacao += delta_time

        if self.tempo_animacao >= 0.1:

            self.tempo_animacao = 0.0

            self.quadro_atual = (
                self.quadro_atual + 1
            ) % len(self.passos_direita)

        if self.virado_para == "DIREITA":

            self.texture = (
                self.passos_direita[
                    self.quadro_atual
                ]
            )

        else:

            self.texture = (
                self.passos_esquerda[
                    self.quadro_atual
                ]
            )

    def jump(self):

        if self.virado_para == "DIREITA":

            self.texture = self.textura_pulo_d

        else:

            self.texture = self.textura_pulo_e

    def idle(self):        
        self.quadro_atual = 0

        if self.virado_para == "DIREITA":

            self.texture = self.textura_parado_d

        else:
            self.texture = self.textura_parado_e

class Moeda(arcade.Sprite):

    def __init__(self):
        super().__init__(
            os.path.join(ASSETS_DIR, "MOEDA.png"),
            scale=0.02
        )

class MoedaEspecial(arcade.Sprite):

    def __init__(self):
        super().__init__(
            os.path.join(ASSETS_DIR, "MOEDA.png"),
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
            os.path.join(ASSETS_DIR, "kuromi.png"),
            scale=0.15
        )

        self.change_x = 100

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
            os.path.join(ASSETS_DIR, "melody.png"),
            scale=0.25
        )

        self.velocidade = 50
        self.change_x = 0

    def perseguir_jogador(self, jogador):
        if jogador.center_x > self.center_x:
            self.change_x = self.velocidade

        elif jogador.center_x < self.center_x:
            self.change_x = -self.velocidade

        else:
            self.change_x = 0

        if jogador.center_y > self.center_y:
            self.change_y = self.velocidade
        elif jogador.center_y < self.center_y:
            self.change_y = -self.velocidade
        else:
            self.change_y = 0

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

class Bloco(arcade.Sprite):

    def __init__(self, escala=0.35):
        super().__init__(
            os.path.join(ASSETS_DIR, "bloco.png"),
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

        self.explosion = arcade.Sprite(os.path.join(ASSETS_DIR, "explosion.png"))

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
            (100, 380),
            (300, 250),
            (500, 180),
            (700, 320),
            (900, 380),
            (1100, 250),
            (1300, 180),
            (1500, 320),
        ]

        for x, y in plataformas:
            bloco = Bloco(
                escala=0.3
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
            (850, 150),
            (1050, 220),
            (1250, 130),
            (1500, 180),
            (1700, 300),
            (900, 400),
            (1100, 250),
            (1350, 350),
            (1600, 450),
            (1750, 200),
            (150, 450),
            (400, 350),
            (650, 150),
            (850, 480),
            (1100, 400),
            (1300, 250),
            (1500, 350),
            (1700, 480),
            (350, 200),
            (700, 500),
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

        inimigo.center_x = 20
        inimigo.center_y = 100

        self.sprite_inimigos.append(
            inimigo
        )

        self.inimigo_especial = InimigoEspecial()

        self.inimigo_especial.center_x = 700
        self.inimigo_especial.center_y = 500

        self.sprite_inimigos_especiais.append(
            self.inimigo_especial
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
            ALTURA - 20,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            f"Tempo: {self.tempo:.1f}s",
            LARGURA - 200,
            ALTURA - 20,
            arcade.color.WHITE,
            20
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

        self.sprite_inimigos_especiais.update()

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

                if self.explosion not in self.sprite_inimigos:

                    self.explosion.center_x = inimigo.center_x
                    self.explosion.center_y = inimigo.center_y

                    
                    self.sprite_inimigos.append(
                        self.explosion
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

        if self.explosion in self.sprite_inimigos:
            if self.tempo_invulnerabilidade <= 0:
                self.explosion.remove_from_sprite_lists()
            else:
                self.explosion.scale = 0.1 + 0.05 * (self.tempo_invulnerabilidade) * 8

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
                self.jogador.change_y = 20

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

        if os.path.exists(os.path.join(ASSETS_DIR, "melody.png")):

            avatar1 = arcade.Sprite(
                os.path.join(ASSETS_DIR, "melody.png"),
                scale=0.5
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
        sofreu_dano):

        super().__init__()

        self.pontuacao = pontuacao
        self.tempo = tempo
        self.sofreu_dano = sofreu_dano
        self.nome_digitado = ""
        self.LIMITE_NOME = 12
    
    def on_text(self, text):
        if text.isprintable() and len(self.nome_digitado) < self.LIMITE_NOME:
            self.nome_digitado += text


    def on_key_press(self, key, modifiers):

        if key == arcade.key.BACKSPACE:
            self.nome_digitado = self.nome_digitado[:-1]

        elif key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:
            nome = self.nome_digitado.strip()

            if nome:
                nova = self.salvar_pontuacao(nome)
                print(f"Pontuação salva: {nova}")

                self.window.show_view(TelaInicial())

        elif key == arcade.key.M:
            self.window.show_view(TelaInicial())

        elif key == arcade.key.ESCAPE:
            arcade.close_window()


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
        
                # Rótulo acima da caixa
        arcade.draw_text("Digite seu nome para o ranking:", LARGURA / 2, 270,
                         arcade.color.WHITE, 16, anchor_x="center")

        # Contorno da caixa: XYWH descreve o retângulo pelo centro e pelas dimensões
        arcade.draw_rect_outline(arcade.XYWH(LARGURA / 2, 222, 360, 50),
                                 arcade.color.WHITE, border_width=2)

        # O texto digitado, centralizado dentro da caixa (anchor_y="center")
        arcade.draw_text(self.nome_digitado + "_", LARGURA / 2, 222,
                         arcade.color.YELLOW, 22, anchor_x="center", anchor_y="center")

    def salvar_pontuacao(self, nome):
        return Pontuacao.create(
            nome_jogador=nome,
            pontos=self.pontuacao,
            tempo_partida=self.tempo
        )
    
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

        arcade.draw_text(
            "[R] Ranking",
            LARGURA / 2,
            100,
            arcade.color.PURPLE,
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
        elif key == arcade.key.R:
            tela_ranking = TelaRanking()

            self.window.show_view(
                tela_ranking
            )

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class TelaRanking(arcade.View):
    """Exibe as 10 melhores pontuações salvas no banco de dados."""

    def __init__(self, destaque_id: int = None):
        super().__init__()
        # A consulta roda UMA vez, aqui no construtor — nunca no on_draw()
        self.melhores = buscar_top10()
        # id da partida que acabou de ser salva (None quando viemos do menu)
        self.destaque_id = destaque_id

    def on_draw(self):
        self.clear()

                # Caso especial: banco ainda vazio (o for não executaria nenhuma vez)
        if len(self.melhores) == 0:
            arcade.draw_text("Nenhuma pontuação ainda! Seja o primeiro.", LARGURA / 2, 320,
                             arcade.color.WHITE, 20, anchor_x="center")
            return
        


        for indice, p in enumerate(self.melhores):
            if p.id == self.destaque_id:
                cor = arcade.color.YELLOW
            else:
                cor = arcade.color.WHITE
            # índice 0 → y = 440 | índice 1 → y = 406 | índice 2 → y = 372 ...
            y = 440 - indice * 34
            arcade.draw_text(f"{indice + 1}º", 100, y, arcade.color.WHITE, 16)
            arcade.draw_text(p.nome_jogador, 160, y, arcade.color.WHITE, 16)
        
        arcade.draw_text(str(p.pontos), 450, y, cor, 16, anchor_x="right")
        arcade.draw_text(f"{p.tempo_partida:.1f}s", 560, y, cor, 16, anchor_x="right")
        # data_hora volta do banco como um objeto datetime: strftime formata como texto
        arcade.draw_text(p.data_hora.strftime("%d/%m/%Y"), 700, y, cor, 16, anchor_x="right")


    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

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
