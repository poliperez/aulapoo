import arcade
import random
import os


LARGURA = 800
ALTURA = 600
TITULO = "Coletor de Moedas"


# ============================================================
# PLAYER
# ============================================================

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("Hello_Kitty.png", scale=0.1)

        self.textura_direita = arcade.load_texture(
            "Hello_Kitty.png"
        )

        self.textura_esquerda = arcade.load_texture(
            "Hello_Kitty_esp.png"
        )

    def update(self, delta_time):
        # A PhysicsEnginePlatformer controla o movimento.
        # Aqui cuidamos apenas da troca de textura.

        if self.change_x > 0:
            self.texture = self.textura_direita

        elif self.change_x < 0:
            self.texture = self.textura_esquerda


# ============================================================
# MOEDA NORMAL
# ============================================================

class Moeda(arcade.Sprite):

    def __init__(self):
        super().__init__("MOEDA.png", scale=0.02)


# ============================================================
# MOEDA ESPECIAL
# ============================================================

class MoedaEspecial(arcade.Sprite):

    def __init__(self):
        super().__init__("MOEDA.png", scale=0.03)

        self.change_x = 150
        self.change_y = 100

    def update(self, delta_time):

        # Movimento
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Rebote no eixo X
        if self.right >= LARGURA:
            self.right = LARGURA
            self.change_x *= -1

        elif self.left <= 0:
            self.left = 0
            self.change_x *= -1

        # Rebote no eixo Y
        if self.top >= ALTURA:
            self.top = ALTURA
            self.change_y *= -1

        elif self.bottom <= 0:
            self.bottom = 0
            self.change_y *= -1


# ============================================================
# INIMIGO
# ============================================================

class Inimigo(arcade.Sprite):

    def __init__(self):
        super().__init__("kuromi.png", scale=0.3)

        # Velocidade horizontal do inimigo
        self.change_x = 150

    def update(self, delta_time):

        # Movimento horizontal
        self.center_x += self.change_x * delta_time

        # Rebote na borda direita
        if self.right >= LARGURA:
            self.right = LARGURA
            self.change_x *= -1

        # Rebote na borda esquerda
        elif self.left <= 0:
            self.left = 0
            self.change_x *= -1


# ============================================================
# INIMIGO ESPECIAL
# ============================================================

class InimigoEspecial(arcade.Sprite):

    def __init__(self):
        super().__init__("kuromi.png", scale=0.25)

        # Velocidade de perseguição
        self.velocidade = 100

        # Velocidade horizontal usada pela física
        self.change_x = 0

    def perseguir_jogador(self, jogador):

        # Jogador está à direita
        if jogador.center_x > self.center_x:
            self.change_x = self.velocidade

        # Jogador está à esquerda
        elif jogador.center_x < self.center_x:
            self.change_x = -self.velocidade

        # Jogador está praticamente na mesma posição
        else:
            self.change_x = 0


# ============================================================
# BLOCO
# ============================================================

class Bloco(arcade.Sprite):

    def __init__(self):
        super().__init__("bloco.png", scale=0.5)


# ============================================================
# TELA DE JOGO
# ============================================================

class TelaJogo(arcade.View):

    def __init__(self):

        super().__init__()

        arcade.set_background_color(
            arcade.color.PINK
        )

        # ----------------------------------------------------
        # Estados do jogo
        # ----------------------------------------------------

        self.pontuacao = 0
        self.tempo = 0

        # Indica se o jogador já sofreu dano
        self.sofreu_dano = False

        # Texto de alerta
        self.alerta = ""

        # Tempo que o alerta permanece na tela
        self.tempo_alerta = 0

        # Tempo de invulnerabilidade depois de uma colisão
        self.tempo_invulnerabilidade = 0

        # ----------------------------------------------------
        # SpriteLists
        # ----------------------------------------------------

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_moeda_especial = arcade.SpriteList()
        self.sprite_blocos = arcade.SpriteList()
        self.sprite_inimigos = arcade.SpriteList()

        # SpriteList do InimigoEspecial
        self.sprite_inimigos_especiais = arcade.SpriteList()

        # ----------------------------------------------------
        # PLAYER
        # ----------------------------------------------------

        self.jogador = Player()

        self.jogador.center_x = 400
        self.jogador.center_y = 150

        self.sprite_jogador.append(
            self.jogador
        )

        # ----------------------------------------------------
        # CHÃO
        # ----------------------------------------------------

        for x in range(40, LARGURA, 80):

            bloco = Bloco()

            bloco.center_x = x
            bloco.center_y = 25

            self.sprite_blocos.append(
                bloco
            )

        # ----------------------------------------------------
        # PLATAFORMAS
        # ----------------------------------------------------

        plataformas = [
            (200, 150),
            (400, 250),
            (600, 150),
            (650, 350)
        ]

        for x, y in plataformas:

            bloco = Bloco()

            bloco.center_x = x
            bloco.center_y = y

            self.sprite_blocos.append(
                bloco
            )

        # ----------------------------------------------------
        # PHYSICS ENGINE DO PLAYER
        # ----------------------------------------------------

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.jogador,
            platforms=self.sprite_blocos,
            gravity_constant=1
        )

        # ----------------------------------------------------
        # 25 MOEDAS NORMAIS
        # ----------------------------------------------------

        for i in range(25):

            moeda = Moeda()

            moeda.center_x = random.randint(
                50,
                750
            )

            moeda.center_y = random.randint(
                80,
                550
            )

            self.sprite_moedas.append(
                moeda
            )

        # ----------------------------------------------------
        # MOEDA ESPECIAL
        # ----------------------------------------------------

        self.moeda_especial = MoedaEspecial()

        self.moeda_especial.center_x = 650
        self.moeda_especial.center_y = 500

        self.sprite_moeda_especial.append(
            self.moeda_especial
        )

        # ----------------------------------------------------
        # INIMIGO COMUM
        # ----------------------------------------------------

        inimigo = Inimigo()

        inimigo.center_x = 200
        inimigo.center_y = 100

        self.sprite_inimigos.append(
            inimigo
        )

        # ----------------------------------------------------
        # INIMIGO ESPECIAL
        # ----------------------------------------------------

        self.inimigo_especial = InimigoEspecial()

        self.inimigo_especial.center_x = 600
        self.inimigo_especial.center_y = 100

        self.sprite_inimigos_especiais.append(
            self.inimigo_especial
        )

        # ----------------------------------------------------
        # PHYSICS ENGINE DO INIMIGO ESPECIAL
        # ----------------------------------------------------
        #
        # IMPORTANTE:
        # Este bloco fica DEPOIS da criação do
        # self.inimigo_especial.
        #

        self.physics_engine_inimigo_especial = (
            arcade.PhysicsEnginePlatformer(
                self.inimigo_especial,
                platforms=self.sprite_blocos,
                gravity_constant=1
            )
        )

    # ========================================================
    # DESENHAR
    # ========================================================

    def on_draw(self):

        self.clear()

        # Player
        self.sprite_jogador.draw()

        # Moedas
        self.sprite_moedas.draw()

        # Moeda especial
        self.sprite_moeda_especial.draw()

        # Blocos
        self.sprite_blocos.draw()

        # Inimigos
        self.sprite_inimigos.draw()

        # Inimigo especial
        self.sprite_inimigos_especiais.draw()

        # ----------------------------------------------------
        # PONTUAÇÃO
        # ----------------------------------------------------

        arcade.draw_text(
            f"Moedas Coletadas: {self.pontuacao}",
            10,
            570,
            arcade.color.WHITE,
            14
        )

        # ----------------------------------------------------
        # TEMPO
        # ----------------------------------------------------

        arcade.draw_text(
            f"Tempo: {self.tempo:.1f}s",
            650,
            570,
            arcade.color.WHITE,
            14
        )

        # ----------------------------------------------------
        # ALERTA
        # ----------------------------------------------------

        if self.alerta:

            arcade.draw_text(
                self.alerta,
                LARGURA / 2,
                520,
                arcade.color.RED,
                22,
                anchor_x="center"
            )

    # ========================================================
    # ATUALIZAÇÃO DO JOGO
    # ========================================================

    def on_update(self, delta_time):

        # ----------------------------------------------------
        # TEMPO
        # ----------------------------------------------------

        self.tempo += delta_time

        # ----------------------------------------------------
        # ATUALIZAR PLAYER
        # ----------------------------------------------------

        self.sprite_jogador.update(
            delta_time
        )

        # ----------------------------------------------------
        # ATUALIZAR FÍSICA DO PLAYER
        # ----------------------------------------------------

        self.physics_engine.update()

        # ----------------------------------------------------
        # ATUALIZAR MOEDA ESPECIAL
        # ----------------------------------------------------

        self.sprite_moeda_especial.update(
            delta_time
        )

        # ----------------------------------------------------
        # ATUALIZAR INIMIGOS COMUNS
        # ----------------------------------------------------

        self.sprite_inimigos.update(
            delta_time
        )

        # ----------------------------------------------------
        # ATUALIZAR INIMIGO ESPECIAL
        # ----------------------------------------------------

        self.inimigo_especial.perseguir_jogador(
            self.jogador
        )

        self.physics_engine_inimigo_especial.update()

        # ----------------------------------------------------
        # ATUALIZAR INVULNERABILIDADE
        # ----------------------------------------------------

        if self.tempo_invulnerabilidade > 0:

            self.tempo_invulnerabilidade -= delta_time

        # ----------------------------------------------------
        # ATUALIZAR ALERTA
        # ----------------------------------------------------

        if self.tempo_alerta > 0:

            self.tempo_alerta -= delta_time

        else:

            self.alerta = ""

        # ----------------------------------------------------
        # COLISÃO COM MOEDAS NORMAIS
        # ----------------------------------------------------

        moedas_colididas = (
            arcade.check_for_collision_with_list(
                self.jogador,
                self.sprite_moedas
            )
        )

        for moeda in moedas_colididas:

            # A moeda é removida porque é descartável
            moeda.remove_from_sprite_lists()

            # +1 ponto
            self.pontuacao += 1

        # ----------------------------------------------------
        # COLISÃO COM MOEDA ESPECIAL
        # ----------------------------------------------------

        moedas_especiais_colididas = (
            arcade.check_for_collision_with_list(
                self.jogador,
                self.sprite_moeda_especial
            )
        )

        for moeda in moedas_especiais_colididas:

            # A moeda especial também é descartável
            moeda.remove_from_sprite_lists()

            # +5 pontos
            self.pontuacao += 5

        # ----------------------------------------------------
        # COLISÃO COM INIMIGO COMUM
        # ----------------------------------------------------

        if self.tempo_invulnerabilidade <= 0:

            inimigos_colididos = (
                arcade.check_for_collision_with_list(
                    self.jogador,
                    self.sprite_inimigos
                )
            )

            for inimigo in inimigos_colididos:

                # Perde 1 ponto
                self.pontuacao -= 1

                # Registra que sofreu dano
                self.sofreu_dano = True

                # Mostra alerta
                self.alerta = (
                    "CUIDADO! Você foi atingido!"
                )

                # Alerta permanece por 2 segundos
                self.tempo_alerta = 2

                # Evita perder vários pontos
                # enquanto permanece encostado
                self.tempo_invulnerabilidade = 1

                # IMPORTANTE:
                # O inimigo NÃO é removido.
                # Ele continua no jogo.

        # ----------------------------------------------------
        # COLISÃO COM INIMIGO ESPECIAL
        # ----------------------------------------------------

        inimigos_especiais_colididos = (
            arcade.check_for_collision_with_list(
                self.jogador,
                self.sprite_inimigos_especiais
            )
        )

        for inimigo in inimigos_especiais_colididos:

            # Perde 1 ponto
            self.pontuacao -= 1

            # Registra que sofreu dano
            self.sofreu_dano = True

            # Mostra alerta
            self.alerta = (
                "CUIDADO! O inimigo especial te encontrou!"
            )

            # Alerta permanece por 2 segundos
            self.tempo_alerta = 2

            # ------------------------------------------------
            # TELETRANSPORTE
            # ------------------------------------------------

            nova_posicao_encontrada = False

            while not nova_posicao_encontrada:

                novo_x = random.randint(
                    50,
                    750
                )

                # Nasce no nível do chão
                novo_y = 100

                # Evita nascer muito perto do jogador
                distancia = abs(
                    novo_x - self.jogador.center_x
                )

                if distancia > 150:

                    nova_posicao_encontrada = True

                    inimigo.center_x = novo_x
                    inimigo.center_y = novo_y

            # Zera a velocidade antes de continuar
            # a perseguição.

            inimigo.change_x = 0

        # ----------------------------------------------------
        # GAME OVER
        # ----------------------------------------------------

        if len(self.sprite_moedas) == 0:

            tela_game_over = TelaGameOver(
                self.pontuacao,
                self.tempo,
                self.sofreu_dano
            )

            self.window.show_view(
                tela_game_over
            )

    # ========================================================
    # TECLAS PRESSIONADAS
    # ========================================================

    def on_key_press(self, key, modifiers):

        # ----------------------------------------------------
        # DIREITA
        # ----------------------------------------------------

        if (
            key == arcade.key.RIGHT
            or key == arcade.key.D
        ):

            self.jogador.change_x = 5

        # ----------------------------------------------------
        # ESQUERDA
        # ----------------------------------------------------

        elif (
            key == arcade.key.LEFT
            or key == arcade.key.A
        ):

            self.jogador.change_x = -5

        # ----------------------------------------------------
        # PULO
        # ----------------------------------------------------

        elif (
            key == arcade.key.UP
            or key == arcade.key.W
        ):

            if self.physics_engine.can_jump():

                self.jogador.change_y = 15

        # ----------------------------------------------------
        # ESC = VOLTAR AO MENU
        # ----------------------------------------------------

        elif key == arcade.key.ESCAPE:

            self.window.show_view(
                TelaInicial()
            )

    # ========================================================
    # TECLAS SOLTAS
    # ========================================================

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


# ============================================================
# TELA SOBRE
# ============================================================

class TelaSobre(arcade.View):

    def __init__(self):

        super().__init__()

        # SpriteList dos avatares
        self.sprite_avatares = arcade.SpriteList()

        # ----------------------------------------------------
        # AVATAR 1
        # ----------------------------------------------------

        if os.path.exists("avatar1.png"):

            avatar1 = arcade.Sprite(
                "avatar1.png",
                scale=0.15
            )

            avatar1.center_x = 200
            avatar1.center_y = 200

            self.sprite_avatares.append(
                avatar1
            )

        # ----------------------------------------------------
        # AVATAR 2
        # ----------------------------------------------------

        if os.path.exists("avatar2.png"):

            avatar2 = arcade.Sprite(
                "avatar2.png",
                scale=0.15
            )

            avatar2.center_x = 400
            avatar2.center_y = 200

            self.sprite_avatares.append(
                avatar2
            )

        # ----------------------------------------------------
        # AVATAR 3
        # ----------------------------------------------------

        if os.path.exists("avatar3.png"):

            avatar3 = arcade.Sprite(
                "avatar3.png",
                scale=0.15
            )

            avatar3.center_x = 600
            avatar3.center_y = 200

            self.sprite_avatares.append(
                avatar3
            )

        # ----------------------------------------------------
        # AVATAR 4
        # ----------------------------------------------------

        if os.path.exists("avatar4.png"):

            avatar4 = arcade.Sprite(
                "avatar4.png",
                scale=0.15
            )

            avatar4.center_x = 400
            avatar4.center_y = 100

            self.sprite_avatares.append(
                avatar4
            )

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
            "Desenvolvido por:",
            LARGURA // 2,
            330,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        # Desenha os avatares
        self.sprite_avatares.draw()

        arcade.draw_text(
            "SEU NOME / NOME DOS INTEGRANTES",
            LARGURA // 2,
            50,
            arcade.color.PINK,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Voltar ao menu inicial",
            100,
            20,
            arcade.color.WHITE,
            16
        )

    def on_key_press(self, key, modifiers):

        if (
            key == arcade.key.ESCAPE
            or key == arcade.key.M
        ):

            self.window.show_view(
                TelaInicial()
            )


# ============================================================
# TELA DE INSTRUÇÕES
# ============================================================

class TelaInstrucoes(arcade.View):

    def __init__(self):

        super().__init__()

    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "INSTRUÇÕES",
            LARGURA / 2,
            480,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Objetivo: coletar todas as moedas espalhadas pelo mapa.",
            LARGURA / 2,
            410,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "A / ← : mover para a esquerda",
            LARGURA / 2,
            350,
            arcade.color.LIGHT_SEA_GREEN,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "D / → : mover para a direita",
            LARGURA / 2,
            315,
            arcade.color.LIGHT_SEA_GREEN,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "W / ↑ : pular",
            LARGURA / 2,
            280,
            arcade.color.LIGHT_SEA_GREEN,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Moeda normal: +1 ponto",
            LARGURA / 2,
            225,
            arcade.color.LIGHT_SEA_GREEN,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Moeda especial: +5 pontos",
            LARGURA / 2,
            190,
            arcade.color.LIGHT_SEA_GREEN,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Cuidado com os inimigos: eles retiram 1 ponto!",
            LARGURA / 2,
            155,
            arcade.color.RED,
            17,
            anchor_x="center"
        )

        # ----------------------------------------------------
        # INIMIGO ESPECIAL
        # ----------------------------------------------------

        arcade.draw_text(
            "Inimigo especial: persegue você pelo chão e",
            LARGURA / 2,
            120,
            arcade.color.RED,
            15,
            anchor_x="center"
        )

        arcade.draw_text(
            "se teletransporta para outro ponto após a colisão.",
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


# ============================================================
# TELA GAME OVER
# ============================================================

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
            arcade.color.GOLD,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Pontuação final: {self.pontuacao}",
            LARGURA / 2,
            340,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Tempo total: {self.tempo:.1f} segundos",
            LARGURA / 2,
            290,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        # Se não sofreu nenhum dano,
        # mostra a mensagem especial.

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
                arcade.color.WHITE,
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


# ============================================================
# TELA INICIAL
# ============================================================

class TelaInicial(arcade.View):

    def __init__(self):

        super().__init__()

    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "COLETOR DE MOEDAS",
            LARGURA / 2,
            420,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "[J] Jogar",
            LARGURA / 2,
            320,
            arcade.color.LIGHT_SEA_GREEN,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[I] Instruções",
            LARGURA / 2,
            270,
            arcade.color.LIGHT_SEA_GREEN,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[S] Sobre o Jogo",
            LARGURA / 2,
            220,
            arcade.color.LIGHT_SEA_GREEN,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair",
            LARGURA / 2,
            170,
            arcade.color.LIGHT_SEA_GREEN,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        # Jogar
        if key == arcade.key.J:

            tela_jogo = TelaJogo()

            self.window.show_view(
                tela_jogo
            )

        # Instruções
        elif key == arcade.key.I:

            tela_instrucoes = TelaInstrucoes()

            self.window.show_view(
                tela_instrucoes
            )

        # Sobre
        elif key == arcade.key.S:

            tela_sobre = TelaSobre()

            self.window.show_view(
                tela_sobre
            )

        # Sair
        elif key == arcade.key.ESCAPE:

            arcade.close_window()


# ============================================================
# EXECUTAR
# ============================================================

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


# ============================================================
# INÍCIO DO PROGRAMA
# ============================================================

if __name__ == "__main__":
    executar()