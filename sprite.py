from turtle import *
import time

def can_move(obj, new_x, new_y, walls):
    object_radius = getattr(obj, 'radius', 15)
    
    for wall_x1, wall_y1, wall_x2, wall_y2, wall_thickness in walls:
        half_thickness = wall_thickness / 2
        
        if wall_y1 == wall_y2:
            wall_left = min(wall_x1, wall_x2) - half_thickness
            wall_right = max(wall_x1, wall_x2) + half_thickness
            
            if (wall_left <= new_x <= wall_right and 
                abs(new_y - wall_y1) <= object_radius + half_thickness):
                return False
        else:
            wall_bottom = min(wall_y1, wall_y2) - half_thickness
            wall_top = max(wall_y1, wall_y2) + half_thickness
            if (wall_bottom <= new_y <= wall_top and 
                abs(new_x - wall_x1) <= object_radius + half_thickness):
                return False
    return True

class Sprite(Turtle):
    def __init__(self, coords, color, shape, size, name, walls_list):
        super().__init__()
        self.walls = walls_list
        self.up()
        self.goto(coords)
        self.color(color)
        self.shape(shape)
        self.shapesize(size)
        self.step = 6
        self.name = name
        self.name_disp = Turtle()
        self.name_disp.hideturtle()
        self.name_disp.up()
        self.update_name()
        
        # Для управления движением
        self.requested_direction = None
        self.current_direction = None
        self.last_move_time = 0
        self.move_delay = 0.08

    def update_name(self):
        self.name_disp.clear()
        self.name_disp.goto(self.xcor(), self.ycor() + 65)
        self.name_disp.write(self.name, align="center", font=("Arial", 15, "normal"))

    def is_collide(self, other):
        return self.distance(other) < 50

    def move(self, heading):
        old = (self.xcor(), self.ycor())
        self.setheading(heading)
        self.forward(self.step)
        if not can_move(self, self.xcor(), self.ycor(), self.walls):
            self.goto(old)
        self.update_name()

    def process_movement(self):
        """Обрабатывает движение с ограничением частоты"""
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_delay:
            if self.requested_direction is not None:
                self.current_direction = self.requested_direction
                self.move(self.current_direction)
                self.last_move_time = current_time

    # Управление направлением
    def request_direction(self, heading):
        """Запрос на движение в определенном направлении"""
        self.requested_direction = heading
    
    def start_move_up(self):
        self.request_direction(90)
    
    def start_move_down(self):
        self.request_direction(270)
    
    def start_move_left(self):
        self.request_direction(180)
    
    def start_move_right(self):
        self.request_direction(0)
    
    def stop_move_up(self):
        if self.requested_direction == 90:
            self.requested_direction = None
    
    def stop_move_down(self):
        if self.requested_direction == 270:
            self.requested_direction = None
    
    def stop_move_left(self):
        if self.requested_direction == 180:
            self.requested_direction = None
    
    def stop_move_right(self):
        if self.requested_direction == 0:
            self.requested_direction = None

class Enemy(Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, color, shape, size, id, walls_list):
        super().__init__((start_x, start_y), color, shape, size, f"Враг {id}", walls_list)
        self.start_x, self.start_y = start_x, start_y
        self.end_x, self.end_y = end_x, end_y
        self.target_x, self.target_y = end_x, end_y
        self.step = 3
        self.move_delay = 0.0005

    def move_auto(self):
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_delay:
            self.setheading(self.towards(self.target_x, self.target_y))
            self.forward(self.step)
            self.update_name()
            self.last_move_time = current_time
            
            if self.distance(self.target_x, self.target_y) < self.step:
                if self.target_x == self.end_x and self.target_y == self.end_y:
                    self.target_x, self.target_y = self.start_x, self.start_y
                else:
                    self.target_x, self.target_y = self.end_x, self.end_y

def levelsprite(level, walls_list):
    if level == 1:
        player = Sprite((-850, 250), "orange", "turtle", 2, "Игрок", walls_list)
        player.move_delay = 0.001
        enemies = [
            Enemy(-850, 350, 150, 350, "red", "turtle", 4, 1, walls_list),
            Enemy(-150, 350, -150, -350, "red", "turtle", 4, 2, walls_list),
            Enemy(-450, -50, -150, -50, "red", "turtle", 4, 3, walls_list),
            Enemy(-550, -450, 50, -450, "red", "turtle", 4, 4, walls_list),
            Enemy(-850, 50, -550, 50, "red", "turtle", 4, 5, walls_list),
            Enemy(-850, -450, -850, -50, "red", "turtle", 4, 6, walls_list),
            Enemy(450, -450, 850, -450, "red", "turtle", 4, 7, walls_list),
            Enemy(350, 450, 350, -450, "red", "turtle", 4, 8, walls_list),
            Enemy(350, 250, 850, 250, "red", "turtle", 4, 9, walls_list)
        ]
    elif level == 2:
        player = Sprite((-850, 250), "orange", "turtle", 2, "Игрок", walls_list)
        player.move_delay = 0.001
        enemies = []
    else:
        player = None
        enemies = []
    return player, enemies