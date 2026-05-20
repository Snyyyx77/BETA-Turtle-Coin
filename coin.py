from turtle import *
import os
import sys

class Coin(Turtle):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.speed(0)
        self.penup()
        self.goto(x, y)
        self.coins_collected = False

        screen = Screen()
        screen.addshape(image_path)
        self.shape(image_path)
        self.shapesize(2, 2)

    def collect(self):
        self.hideturtle()
        self.coins_collected = True

    def is_collected(self):
        return self.coins_collected

def get_data_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "data", relative_path)

coin_path = get_data_path("coin.gif")
coins = None
def addcoin(corX, corY):
    coin = Coin(corX, corY, coin_path)
    coins.append(coin)
    return coin

def all_coins_collected():
    if coins is None:
        return False
    if not coins:
        return False
    for coin in coins:
        if not coin.is_collected():
            return False
    return True
coins = []
def coinlevel(level):
    if level == 1:
        addcoin(-850, 450)
        addcoin(150, 450)
        addcoin(50, 150)
        addcoin(-350, 50)
        addcoin(-250, -250)
        addcoin(-550, 150)
        addcoin(-650, 150)
        addcoin(-750, -150)
        addcoin(-750, -350)
        addcoin(150, -250)
        addcoin(450, -250)
        addcoin(750, -350)
        addcoin(750, 350)
        addcoin(750, 50)
    elif level == 2:
        addcoin(750, -350)
        print(f"{__name__},Такого уровня пока что нет")
    else:
        print(f"{__name__},Такого уровня пока что нет")

def check_coin_collision(player):
    for coin in coins:
        if not coin.is_collected() and player.distance(coin) < 40:
            coin.collect()
            print("Монета собрана!")
            return True
    return False