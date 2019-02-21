import arcade
import random

THRESHOLD = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
bronzeSprite = "Sprites/coins/Bronze/Bronze_30.png"
silverSprite = "Sprites/coins/Silver/Silver_21.png"
goldSprite = "Sprites/coins/Gold/Gold_21.png"
coinScaling = .05
UPGRADEBOX_UPPER = SCREEN_HEIGHT//4

class Coin(object):
    def __init__(self,name,value):
        self.name = name
        self.value = value

        

class BronzeCoins(Coin):
    def __init__(self):
        super().__init__("Bronze",1)
        self.coinList = arcade.SpriteList()

    def spawn(self,number):
        for i in range(number):
            coin = arcade.Sprite(bronzeSprite,coinScaling)
            coin.center_x = random.randrange(0+coin.width//2,SCREEN_WIDTH-coin.width//2)
            coin.center_y = random.randrange(UPGRADEBOX_UPPER+coin.height//2,SCREEN_HEIGHT-coin.height//2)
            self.coinList.append(coin)

class SilverCoins(Coin):
    def __init__(self):
        super().__init__("Silver",5)
        self.coinList = arcade.SpriteList()

    def spawn(self,number):
        for i in range(number):
            coin = arcade.Sprite(silverSprite,coinScaling)
            coin.center_x = random.randrange(0+coin.width//2,SCREEN_WIDTH-coin.width//2)
            coin.center_y = random.randrange(UPGRADEBOX_UPPER+coin.height//2,SCREEN_HEIGHT-coin.height//2)
            self.coinList.append(coin)

class GoldCoins(Coin):
    def __init__(self):
        super().__init__("Gold",10)
        self.coinList = arcade.SpriteList()

    def spawn(self,number):
        for i in range(number):
            coin = arcade.Sprite(goldSprite,coinScaling)
            coin.center_x = random.randrange(0+coin.width//2,SCREEN_WIDTH-coin.width//2)
            coin.center_y = random.randrange(UPGRADEBOX_UPPER+coin.height//2,SCREEN_HEIGHT-coin.height//2)
            self.coinList.append(coin)
        

class myGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width,height)
        
        self.coinList = None
        self.coinSpriteList = None

        self.Bronze = BronzeCoins()
        self.Silver = SilverCoins()
        self.Gold = GoldCoins()
        
        self.money = 0
        
        arcade.set_background_color(arcade.color.AMAZON)
        


        
    def setup(self):
        
        self.Bronze.spawn(1)
        self.Silver.spawn(2)
        self.Gold.spawn(3)
        
        
        
        
    def on_draw(self):
        arcade.start_render()


        arcade.draw_commands.draw_lrtb_rectangle_filled(0,SCREEN_WIDTH,UPGRADEBOX_UPPER,0,arcade.color.GRAY)

        
        self.Bronze.coinList.draw()
        self.Silver.coinList.draw()
        self.Gold.coinList.draw()

        
    def update(self, delta_time):
            
        self.Bronze.coinList.update()
        self.Silver.coinList.update()
        self.Gold.coinList.update()

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        pass


    def on_key_release(self,key,modifiers):
        pass


            
def main():
    game = myGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
