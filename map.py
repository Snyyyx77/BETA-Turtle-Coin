from turtle import *
from level_coords.levels import LEVEL_WALLS

def paintWall(stylus, start, end, size, walls_list): 
    stylus.pensize(size)
    stylus.penup()
    stylus.goto(start)
    stylus.pendown()
    stylus.goto(end)
    stylus.hideturtle()
    
    walls_list.append((start[0], start[1], end[0], end[1], size))

def levelmap(level, walls_list):
    walls_list.clear()
    
    stylus = Turtle()
    stylus.speed(0)
    stylus.hideturtle()
    
    # Границы
    paintWall(stylus, (-900, 500), (900, 500), 10, walls_list)
    paintWall(stylus, (-900, -500), (900, -500), 10, walls_list)
    paintWall(stylus, (-900, 500), (-900, -500), 10, walls_list)
    paintWall(stylus, (900, 500), (900, -500), 10, walls_list)
    
    # Стены уровня
    walls_data = LEVEL_WALLS.get(level)
    if walls_data is None:
        print(f"{__name__},Такого уровня пока что нет")
    else:
        for start, end in walls_data:
            paintWall(stylus, start, end, 5, walls_list)
    
    Screen().update()