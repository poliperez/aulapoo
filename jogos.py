import arcade

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Hello_Kitty.png", 0.3)
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if(self.change_x>0):
            self.texture= self.textura_direita
        elif(self.change_x<0):
            self.texture = self.textura_esquerda

        

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "jogos")
        arcade.set_background_color(arcade.color.AMAZON)
        self.movimento=2
        self.obj_list = arcade.SpriteList()
        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 300
        self.obj_list.append(self.jogador)

    def on_draw(self):
        self.clear()
        self.obj_list.draw()

window = JanelaJogo()
arcade.run()    

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("MOEDA.png", scale=0.5)
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x>800:
            self.change_x=0

        elif self.center_x<0:
            self.change_x=0
        
        if self.center_y>600:
            self.change_y=0

        elif self.bottom <0:
            self.change_y=0
      


