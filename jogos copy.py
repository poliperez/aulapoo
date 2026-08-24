import arcade
import random

LARGURA = 800
ALTURA = 600
TITULO = "Coletor de Moedas"

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Hello_Kitty.png", scale=0.5)

        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture("Hello_Kitty.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

            if self.right > 800:
                 self.right = 800
                 self.change_x = 0
            if self.top > 600:
                 self.top = 600
                 self.change_y = 0
            if self.left < 0:
                 self.left = 0
                 self.change_x = 0
            if self.bottom < 0:
                 self.bottom = 0
                 self.change_y = 0

    
       
class Moeda(arcade.Sprite):
     def __init__(self):
        super().__init__("MOEDA.png", scale=0.1)

     def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        
        if self.left < 0 or self.right > 800:
           self.change_x *= -1  
# Rebote no Eixo Y
        if self.bottom < 0 or self.top > 600:
          self.change_y *= -1 

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
      super().__init__("MOEDA.png", scale=0.6) # escala maior
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Rebote no Eixo X
        if self.left < 0 or self.right > 800:
         self.change_x *= -1  
        # Rebote no Eixo Y
        if self.bottom < 0 or self.top > 600:
         self.change_y *= -1

class TelaInicial(arcade.View):
     def __init__(self):
      super().__init__()
     def on_draw(self):
        self.clear()
        # Desenha textos simples centralizados na tela
        arcade.draw_text("COLETOR DE MOEDAS", LARGURA / 2, 400, arcade.color.WHITE, 32, 
        anchor_x="center")
        arcade.draw_text("Pressione [J] para Jogar", LARGURA / 2, 300, 
        arcade.color.LIGHT_SEA_GREEN, 18, anchor_x="center")
        arcade.draw_text("Pressione [ESC] para Sair", LARGURA / 2, 240, 
        arcade.color.LIGHT_SEA_GREEN, 18, anchor_x="center")
     def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
         tela_jogo = TelaJogo() # Instancia a tela do jogo
         self.window.show_view(tela_jogo) # Encaixa ela na janela ativa
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
     def executar():
    # 1. Cria a estrutura da janela física usando nossas constantes
      janela = arcade.Window(LARGURA, ALTURA, TITULO)
    # 2. Instancia a tela de menu inicial
      menu_inicial = TelaInicial()
    # 3. Alimenta a janela com o menu e roda o loop do jogo
      janela.show_view(menu_inicial)
      arcade.run()
     if __name__ == "__main__":
       executar()

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.PINK)
        self.pontuacao=8
        self.velocidade = 3

        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 300

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.jogador.left = 0
        self.jogador.bottom = 0

        self.moeda = Moeda()
        self.moeda.center_x = 150
        self.moeda.center_y = 100
        self.sprite_moedas = arcade.SpriteList()
        for i in range(25):
             moeda = Moeda()
             moeda.center_x = random.randint(50, 750)
             moeda.center_y = random.randint(50, 550)
        self.sprite_moedas.append(self.moeda)

        self.moeda_especial = MoedaEspecial()
        self.moeda_especial.center_x = 650  
        self.moeda_especial.center_y = 500
        self.moeda_especial.change_x = self.velocidade
        self.moeda_especial.change_y = self.velocidade-1 # Velocidade diferente no eixo y
        self.sprite_moedas.append(self.moeda_especial)

    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.jogador)
        self.sprite_moedas.draw()
        arcade.draw_text(f"Moedas Coletadas: {self.pontuacao}", 10, 570, 
          arcade.color.WHITE, 14)


    def on_update(self, delta_time):
        self.sprite_moedas.update()
        self.sprite_jogador.update()

        moedas_colididas = arcade.check_for_collision_with_list(self.jogador, 
        self.sprite_moedas)
        for moeda in moedas_colididas:
         moeda.remove_from_sprite_lists()
         if moeda == self.moeda_especial:
            self.pontuacao += 5
        else:
            self.pontuacao += 1



    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT: # Seta da esquerda ou A
         self.jogador.change_x += self.velocidade
        elif key == arcade.key.LEFT: # Seta da direita ou D
         self.jogador.change_x -= self.velocidade
        elif key == arcade.key.UP: # Seta de cima ou W
         self.jogador.change_y += self.velocidade
        elif key == arcade.key.DOWN: # Seta de baixo ou s
         self.jogador.change_y -= self.velocidade

        
        if key == arcade.key.ESCAPE: 
          arcade.close_window()

    def on_key_release(self, key, modifiers):
# Ao soltar uma tecla, verifica se é do eixo X ou Y para zerar a velocidade
     if key in [arcade.key.LEFT, arcade.key.RIGHT]:
      self.jogador.change_x = 0
     if key in [arcade.key.UP, arcade.key.DOWN]:
      self.jogador.change_y = 0

