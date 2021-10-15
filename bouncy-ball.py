import tkinter as tk
import time    as tm


# Global Variables
SCALE = 30.0
GRAVITY = 9.8 * SCALE
CANVAS = None
CANVAS_HEIGHT = 600
CANVAS_WIDTH  = 800
DELTA_TIME = 0.01
BOUNCY_BALL_NUM = 5


# Structs
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.left_up      = Point(x1, y1)
        self.right_bottom = Point(x1, y1)

class Bouncy_Ball:
    ''' a physic-based bouncy ball '''

    def __init__(self, radius, x, y, x_speed, y_speed, width=1.0):
        self.radius = radius
        self.center = Point(x, y)
        self.speed  = Point(x_speed, y_speed)
        self.width  = width

        self.bounding_box = Rectangle(x - radius, y - radius, x + radius, y + radius)
        self.id = CANVAS.create_oval(self.bounding_box.x1, self.bounding_box.y1,
                                     self.bounding_box.x2, self.bounding_box.y2,
                                     width=width)

    def update(self):
        delta_speed   = Point(0.0, 0.0)
        delta_speed.x = 0.0
        delta_speed.y = GRAVITY * DELTA_TIME

        self.center.x += (self.speed.x + 0.5 * delta_speed.x) * DELTA_TIME
        self.center.y += (self.speed.y + 0.5 * delta_speed.y) * DELTA_TIME
        self.speed.x += delta_speed.x
        self.speed.y += delta_speed.y

        self.bounding_box = Rectangle(self.center.x - self.radius,
                                      self.center.y - self.radius,
                                      self.center.x + self.radius,
                                      self.center.y + self.radius)

        # need change to use force analysis for real physic-based bouncy ball
        if self.center.x + self.radius > CANVAS_WIDTH or self.center.x - self.radius < 0.0:
            self.speed.x = -self.speed.x
        if self.center.y + self.radius > CANVAS_HEIGHT:
            self.speed.y = -self.speed.y

    def render(self):
        CANVAS.coords(self.id, [self.bounding_box.x1, self.bounding_box.y1,
                                self.bounding_box.x2, self.bounding_box.y2])

    def set_radius(self, radius):
        self.radius = radius

    def set_center(self, x, y):
        self.center.x = x
        self.center.y = y

    def change_radius(self, radius_diff):
        self.radius += radius_diff

    def change_center(self, x_diff, y_diff):
        self.center.x += x_diff
        self.center.y += y_diff


# Tools
def draw_call():
    ''' draw elements on canvas '''
    CANVAS.update_idletasks()
    CANVAS.update()

def update(update_queue):
    ''' object irrelevant update '''
    for update_item in update_queue:
        update_item.update()

def render(render_queue):
    ''' object irrelevant render '''
    for render_item in render_queue:
        render_item.render()

    draw_call()


# Entrance
if __name__ == '__main__':
    board = tk.Tk()
    board.title('bouncy ball')

    CANVAS = tk.Canvas(board, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='ivory')
    CANVAS.pack()

    update_queue = []
    render_queue = []
    for i in range(BOUNCY_BALL_NUM):
        bouncy_ball = Bouncy_Ball(20, 400, 100, -40.0 + i * 20.0, 0.0)
        update_queue.append(bouncy_ball)
        render_queue.append(bouncy_ball)

    while True:
        tm.sleep(DELTA_TIME)

        update(update_queue)
        render(render_queue)

