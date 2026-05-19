from turtle import *
import time
from map import levelmap
from coin import *
from sprite import Enemy, levelsprite, Sprite
import os
import sys

# ДЛЯ РАБОТЫ С ФАЙЛАМИ
def get_data_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "data", relative_path)

image_path = get_data_path("bg.png")

# НАСТРОЙКА ОКНА
def setup_screen():
    screen = Screen()
    screen.setup(0.75, 0.75)
    screen.tracer(0)
    screen.bgcolor("#58751E")
    screen.bgpic(image_path)
    screen.title("TurtleCoin")
    return screen

screen = setup_screen()

def add_outline(turtle_obj):
    if turtle_obj:
        turtle_obj.pencolor("black")
        turtle_obj.turtlesize(outline=2)

def setup_player_controls(player_obj):
    """Настройка управления игроком"""
    screen.onkeypress(player_obj.start_move_up, "Up")
    screen.onkeypress(player_obj.start_move_down, "Down")
    screen.onkeypress(player_obj.start_move_left, "Left")
    screen.onkeypress(player_obj.start_move_right, "Right")
    
    screen.onkeyrelease(player_obj.stop_move_up, "Up")
    screen.onkeyrelease(player_obj.stop_move_down, "Down")
    screen.onkeyrelease(player_obj.stop_move_left, "Left")
    screen.onkeyrelease(player_obj.stop_move_right, "Right")
    screen.listen()

def setup_game_objects(player_obj, enemies_list):
    """Настройка отображения объектов"""
    add_outline(player_obj)
    for enemy in enemies_list:
        add_outline(enemy)
    screen.update()

level = 1
maxlevel = 2
walls = []

def checklevel(level_num, walls_list):
    """Загрузка уровня"""
    levelmap(level_num, walls_list)
    coinlevel(level_num)
    player, enemies = levelsprite(level_num, walls_list)
    if level_num > maxlevel:
        return None, None
    return player, enemies

def restart_level():
    """Перезапуск текущего уровня"""
    global player, enemies, walls, game_over
    screen.clear()
    screen.bgcolor("#58751E")
    screen.bgpic(image_path)
    screen.tracer(0)
    screen.title("TurtleCoin")
    
    walls.clear()
    coins.clear()
    
    player, enemies = checklevel(level, walls)
    if player is None:
        game_over = True
        return
    
    setup_player_controls(player)
    setup_game_objects(player, enemies)
    screen.update()

# Первоначальная загрузка
player, enemies = checklevel(level, walls)
if player is None:
    print("Не удалось загрузить уровень!")
    exit()

setup_player_controls(player)
setup_game_objects(player, enemies)

game_over = False
last_frame_time = time.time()

# ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ
while not game_over:
    current_time = time.time()
    frame_time = current_time - last_frame_time
    
    # Обработка движения игрока (с ограничением частоты)
    player.process_movement()
    
    # Движение врагов
    for enemy in enemies:
        enemy.move_auto()
    
    # Проверка сбора монет
    check_coin_collision(player)
    
    # Проверка завершения уровня
    if all_coins_collected():
        print(f"Уровень {level} пройден!")
        level += 1
        if level > maxlevel:
            print("Поздравляем! Все уровни пройдены! Ты победил!")
            game_over = True
            break
        
        # Переход на следующий уровень
        screen.clear()
        screen.bgcolor("#58751E")
        screen.bgpic(image_path)
        screen.tracer(0)
        walls.clear()
        coins.clear()
        
        player, enemies = checklevel(level, walls)
        if player is None:
            game_over = True
            break
        
        setup_player_controls(player)
        setup_game_objects(player, enemies)
        screen.update()
        last_frame_time = time.time()
        continue
    
    # Проверка столкновения с врагом
    collision = False
    for enemy in enemies:
        if player.is_collide(enemy):
            print(f"Столкновение с врагом! Перезапуск уровня...")
            collision = True
            break
    
    if collision:
        restart_level()
        last_frame_time = time.time()
        continue
    
    screen.update()
    last_frame_time = current_time
    time.sleep(0.015)  # Небольшая задержка для снижения нагрузки CPU

# Завершение игры
player.hideturtle()
for enemy in enemies:
    enemy.hideturtle()
for coin in coins:
    coin.hideturtle()
screen.update()
time.sleep(3)
screen.bye()