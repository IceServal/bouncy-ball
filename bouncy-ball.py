import tkinter as tk
import time    as tm


GRAVITY = 9.8


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


class Bouncy_Ball:
    def __init__(self, canvas, radius, x, y, width=1.0):
        self.canvas = canvas
        self.radius = radius
        self.center = Point(x, y)
        self.width  = width

        self.bounding_box = Rectangle(x - radius, y - radius, x + radius, y + radius)
        self.id = canvas.create_oval(self.bounding_box.x1, self.bounding_box.y1,
                                     self.bounding_box.x2, self.bounding_box.y2,
                                     width=width)

        self.update()
        self.render()

    def move(self, x_diff, y_diff):
        self.set_center(self.center.x + x_diff, self.center.y + y_diff)
        self.update()
        self.render()

    def update(self):
        self.bounding_box= Rectangle(self.center.x - self.radius,
                                     self.center.y - self.radius,
                                     self.center.x + self.radius,
                                     self.center.y + self.radius)

    def render(self):
        self.canvas.coords(self.id, [self.bounding_box.x1, self.bounding_box.y1,
                                     self.bounding_box.x2, self.bounding_box.y2])

    def set_radius(self, radius):
        self.radius = radius

    def set_center(self, x, y):
        self.center.x = x
        self.center.y = y


if __name__ == '__main__':
    board = tk.Tk()
    board.title('bouncy ball')

    canvas = tk.Canvas(board, width=800, height=600, bg='ivory')
    canvas.pack()

    bouncy_ball = Bouncy_Ball(canvas, 20, 100, 100)

    x_offset = 0
    y_offset = 0
    time_pass = 0.0

    while True:
        tm.sleep(0.01)
        time_pass += 0.01

        y_offset = 0.5 * GRAVITY * time_pass * time_pass
        bouncy_ball.move(x_offset, y_offset)
        canvas.update_idletasks()
        canvas.update()

        if bouncy_ball.center.y > 600:
            bouncy_ball.center.y = 0

