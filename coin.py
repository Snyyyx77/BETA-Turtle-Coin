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
        
        # Регистрируем изображение монеты
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
        # Для скомпилированного .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Для обычного запуска
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "data", relative_path)

# Путь к изображению монеты
coin_path = get_data_path("coin.gif")
coins = None
def addcoin(corX, corY):
    coin = Coin(corX, corY, coin_path)
    coins.append(coin)
    return coin

def all_coins_collected():
    if coins is None:  # Проверяем, существует ли список
        return False
    if not coins:       # Если список пустой
        return False
    for coin in coins:
        if not coin.is_collected():
            return False
    return True
coins = []
def coinlevel(level):
    if level == 1:
        addcoin(-850, 450)   # монета 1
        addcoin(150, 450)    # монета 2
        addcoin(50, 150)     # монета 3
        addcoin(-350, 50)    # монета 4
        addcoin(-250, -250)  # монета 5
        addcoin(-550, 150)   # монета 6
        addcoin(-650, 150)   # монета 7
        addcoin(-750, -150)  # монета 8
        addcoin(-750, -350)  # монета 9
        addcoin(150, -250)   # монета 10
        addcoin(450, -250)   # монета 11
        addcoin(750, -350)   # монета 12
        addcoin(750, 350)    # монета 13
        addcoin(750, 50)     # монета 14
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