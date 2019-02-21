import arcade
import random
import time
import math

THRESHOLD = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
bronzeSprite = "Sprites/coins/Bronze/Bronze_30.png"
silverSprite = "Sprites/coins/Silver/Silver_21.png"
goldSprite = "Sprites/coins/Gold/Gold_21.png"
coinScaling = .075
UPGRADEBOX_UPPER = SCREEN_HEIGHT//4
Upgrade_Order = [["Silver","Gold"],[10,200]]

class TextButton:
    """ Text-based button """
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 locked_color=arcade.color.DARK_GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.locked_color = locked_color
        self.button_height = button_height
        self.locked = False
        
    def draw(self):
        """ Draw the button """
        if self.locked:
            faceColor = self.locked_color
        else:
            faceColor = self.face_color
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, faceColor)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False




class UpgradeButton(TextButton):
    def __init__(self,center_x,center_y,text,upgrade,coin,action,cost,textSize=14):
        super().__init__(center_x,center_y,120,60,text,textSize)
        self.action = action
        self.upgrade = upgrade
        self.coin = coin
        self.text = text
        self.cost = cost
        
    def on_release(self):
        super().on_release()
        self.action(self.upgrade)
        if self.upgrade == 2:
            currentCoin = Upgrade_Order[0].index(self.coin)
            if currentCoin == 1:
                self.locked = True
                self.pressed = True
            else:
                self.coin = Upgrade_Order[0][currentCoin+1]
                self.cost = Upgrade_Order[1][currentCoin+1]
                self.text = f"Unlock {self.coin}" + "\n" + f"{self.cost}"

    def updateCost(self,cost):
        if self.upgrade != 2:
            self.cost = cost
            self.text = self.text[:self.text.index('\n')+1] + f"{cost}"

class Coin(object):
    def __init__(self,name,upgradeManager):
        self.name = name
        self.value = 1.1 ** upgradeManager.upgrades[0][name] * upgradeManager.defaultValues[name]
        self.respawnTime = 0.9 ** upgradeManager.upgrades[1][name] * upgradeManager.defaultRespawnTimes[name]
        self.timer = 0
        self.upgradeManager = upgradeManager

    def upgrade(self,upgrade):
        self.upgradeManager.upgradePurchased(upgrade,self.name)
        self.value = 1.1 ** self.upgradeManager.upgrades[0][self.name] * self.upgradeManager.defaultValues[self.name]
        self.respawnTime = 0.9 ** self.upgradeManager.upgrades[1][self.name] * self.upgradeManager.defaultRespawnTimes[self.name]
        
        

            
        

class BronzeCoins(Coin):
    def __init__(self, upgradeManager):
        super().__init__("Bronze",upgradeManager)
        self.coinList = arcade.SpriteList()

    def spawn(self):
        coin = arcade.Sprite(bronzeSprite,coinScaling)
        coin.center_x = random.randrange(0+coin.width//2,SCREEN_WIDTH-coin.width//2)
        coin.center_y = random.randrange(UPGRADEBOX_UPPER+coin.height//2,SCREEN_HEIGHT-coin.height//2)
        self.coinList.append(coin)

    def refresh(self,dt):
        if self.upgradeManager.upgrades[2][self.name]:
            self.timer += dt
            while self.timer >= self.respawnTime:
                self.timer -= self.respawnTime
                self.spawn()

class SilverCoins(Coin):
    def __init__(self,upgradeManager):
        super().__init__("Silver",upgradeManager)
        self.coinList = arcade.SpriteList()
        self.unlocked = False

    def spawn(self):
        coin = arcade.Sprite(silverSprite,coinScaling)
        coin.center_x = random.randrange(0+coin.width//2,SCREEN_WIDTH-coin.width//2)
        coin.center_y = random.randrange(UPGRADEBOX_UPPER+coin.height//2,SCREEN_HEIGHT-coin.height//2)
        self.coinList.append(coin)

    def refresh(self,dt):
        if self.upgradeManager.upgrades[2][self.name]:
            self.timer += dt
            while self.timer >= self.respawnTime:
                self.timer -= self.respawnTime
                self.spawn()

class GoldCoins(Coin):
    def __init__(self,upgradeManager):
        super().__init__("Gold",upgradeManager)
        self.coinList = arcade.SpriteList()
        self.unlocked = False

    def spawn(self):
        coin = arcade.Sprite(goldSprite,coinScaling)
        coin.center_x = random.randrange(0+coin.width//2,SCREEN_WIDTH-coin.width//2)
        coin.center_y = random.randrange(UPGRADEBOX_UPPER+coin.height//2,SCREEN_HEIGHT-coin.height//2)
        self.coinList.append(coin)

    def refresh(self,dt):
        if self.upgradeManager.upgrades[2][self.name]:
            self.timer += dt
            while self.timer >= self.respawnTime:
                self.timer -= self.respawnTime
                self.spawn()

            
class coinUpgradeManager(object):
    
    def __init__(self):
        #0 index is coin value, 1 index is respawn time, 2 is unlocked
        self.upgrades = [{"Bronze":0,"Silver":0,"Gold":0},{"Bronze":0,"Silver":0,"Gold":0},{"Bronze":True,"Silver":False,"Gold":False}]
        self.defaultRespawnTimes = {"Bronze":2.2,"Silver":11,"Gold":22}
        self.defaultValues = {"Bronze":1,"Silver":5,"Gold":10}
        self.upgradeCosts = [{"Bronze":10,"Silver":100,"Gold":300},{"Bronze":5,"Silver":15,"Gold":45},{"Bronze":0,"Silver":10,"Gold":200}]

    def upgradePurchased(self,upgrade,coin):
        if upgrade == 0 or upgrade == 1:
            self.upgrades[upgrade][coin] += 1
            self.upgradeCosts[upgrade][coin] = math.ceil(1.3*self.upgradeCosts[upgrade][coin])
            
        else:
            self.upgrades[upgrade][coin] = True
      
        print(self.upgrades)

        

class myGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width,height)
        
        self.coinList = None
        self.coinSpriteList = None
        
        self.Bronze = None
        self.Silver = None
        self.Gold = None


        self.player = None
        
        self.startTime = None
        self.money = None
        
        self.coinManager = None

             
        self.buttonList = None
        self.coinTypeButton = None
        
        self.displayPurchaseError = False
        arcade.set_background_color(arcade.color.AMAZON)

      
    def setup(self):
        self.player = arcade.Sprite("Sprites/cursor/cursor.png",.5)
        self.player.center_x = SCREEN_WIDTH//2
        self.player.center_y = SCREEN_HEIGHT//2
        self.startTime = time.time()        
        self.money = int(0)
        self.coinManager = coinUpgradeManager()

        self.set_mouse_visible = False
        
        self.Bronze = BronzeCoins(self.coinManager)
        self.Silver = SilverCoins(self.coinManager)
        self.Gold = GoldCoins(self.coinManager)


        self.buttonList = []

        newline = '\n'
        UnlockButton = UpgradeButton(90,140,f"Unlock Silver{newline}{self.coinManager.upgradeCosts[2]['Silver']}",2,"Silver",self.Silver.upgrade,self.coinManager.upgradeCosts[2]["Silver"])   
        self.buttonList.append(UnlockButton)

        bronzeSpawn = UpgradeButton(230,140,f"Increase Bronze Spawn Rate{newline}{self.coinManager.upgradeCosts[1]['Bronze']}",1,"Bronze",self.Bronze.upgrade,self.coinManager.upgradeCosts[1]["Bronze"],10)
        silverSpawn = UpgradeButton(370,140,f"Increase Silver Spawn Rate{newline}{self.coinManager.upgradeCosts[1]['Silver']}",1,"Silver",self.Silver.upgrade,self.coinManager.upgradeCosts[1]["Silver"],10)
        goldSpawn = UpgradeButton(510,140,f"Increase Gold Spawn Rate{newline}{self.coinManager.upgradeCosts[1]['Gold']}",1,"Gold",self.Gold.upgrade,self.coinManager.upgradeCosts[1]["Gold"],10)

        self.buttonList.append(bronzeSpawn)
        self.buttonList.append(silverSpawn)
        self.buttonList.append(goldSpawn)


        ## ADD in value upgrade buttons ##

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player.center_x = x
        self.player.center_y = y
        
    def on_mouse_press(self, x, y, button, modifiers):
        self.check_mouse_press_for_buttons(x, y)
        self.displayPurchaseError = False

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        self.check_mouse_release_for_buttons(x, y)


    def check_mouse_press_for_buttons(self,x, y):
        for button in self.buttonList:
            if x > button.center_x + button.width / 2:
                continue
            if x < button.center_x - button.width / 2:
                continue
            if y > button.center_y + button.height / 2:
                continue
            if y < button.center_y - button.height / 2:
                continue
            button.on_press()


    def check_mouse_release_for_buttons(self, x, y):
        """ If a mouse button has been released, see if we need to process
        any release events. """
        for button in self.buttonList:
            if button.pressed and not button.locked:
                cost = self.coinManager.upgradeCosts[button.upgrade][button.coin]
                canAfford = (self.money >= cost)
                if canAfford:
                    self.money -= cost
                    button.on_release()
                    button.updateCost(math.ceil(cost*1.3))
                else:
                    button.pressed = False
                    self.displayPurchaseError = True

        
    def on_draw(self):
        arcade.start_render()

        arcade.draw_commands.draw_lrtb_rectangle_filled(0,SCREEN_WIDTH,UPGRADEBOX_UPPER,0,arcade.color.GRAY)

        
        self.Bronze.coinList.draw()
        self.Silver.coinList.draw()
        self.Gold.coinList.draw()
        self.player.draw()
        for i in self.buttonList:
            i.draw()

        output = f"Money: {self.money}"
        arcade.draw_text(output, 20, 780, arcade.color.WHITE, 14)
        if self.displayPurchaseError:
            arcade.draw_text("Insufficient funds", 350,780,arcade.color.RED,14)


        #Debugging Text

        arcade.draw_text(f"BSRate: {self.Bronze.respawnTime}",600,780,arcade.color.WHITE,14)
        arcade.draw_text(f"SSRate: {self.Silver.respawnTime}",600,740,arcade.color.WHITE,14)
        arcade.draw_text(f"GSRate: {self.Gold.respawnTime}",600,700,arcade.color.WHITE,14)
        
    def update(self, delta_time): 
        self.Bronze.refresh(delta_time)
        self.Silver.refresh(delta_time)
        self.Gold.refresh(delta_time)
        
        self.Bronze.coinList.update()
        self.Silver.coinList.update()
        self.Gold.coinList.update()
        self.player.update()

        bronze_coins_hit_list = arcade.check_for_collision_with_list(self.player, self.Bronze.coinList)
        silver_coins_hit_list = arcade.check_for_collision_with_list(self.player, self.Silver.coinList)
        gold_coins_hit_list = arcade.check_for_collision_with_list(self.player, self.Gold.coinList)

        for i in bronze_coins_hit_list:
            self.money += self.Bronze.value
            i.kill()
        
        for i in silver_coins_hit_list:
            self.money += self.Silver.value
            i.kill()
        
        for i in gold_coins_hit_list:
            self.money += self.Gold.value
            i.kill()

            
def main():
    game = myGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
