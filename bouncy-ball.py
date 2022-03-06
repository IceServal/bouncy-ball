import time    as tm
import math    as mt
import tkinter as tk


# Global Variables
PI              = 3.141592654
SCALE           = 40.0
GRAVITY         = 9.8 * SCALE
CANVAS_HEIGHT   = 600
CANVAS_WIDTH    = 800
DELTA_TIME      = 0.01
BOUNCY_BALL_NUM = 5


# Tools
def pow2(x):
    return x * x


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

    def __init__(self, canvas, radius, density, x, y, x_velocity, y_velocity, width=1.0):
        self.radius   = radius
        self.density  = density
        self.mass     = density * PI * pow2(radius)
        self.center   = Point(x, y)
        self.velocity = Point(x_velocity, y_velocity)
        self.width    = width

        self.bounding_box = Rectangle(x - radius, y - radius, x + radius, y + radius)
        self.id = canvas.create_oval(self.bounding_box.x1, self.bounding_box.y1,
                                     self.bounding_box.x2, self.bounding_box.y2,
                                     width=width)

    def update(self):
        delta_velocity   = Point(0.0, 0.0)
        delta_velocity.x = 0.0
        delta_velocity.y = GRAVITY * DELTA_TIME

        self.center.x += (self.velocity.x + 0.5 * delta_velocity.x) * DELTA_TIME
        self.center.y += (self.velocity.y + 0.5 * delta_velocity.y) * DELTA_TIME
        self.velocity.x += delta_velocity.x
        self.velocity.y += delta_velocity.y

        self.bounding_box = Rectangle(self.center.x - self.radius,
                                      self.center.y - self.radius,
                                      self.center.x + self.radius,
                                      self.center.y + self.radius)

        # need change to use force analysis for real physic-based bouncy ball
        if  (self.center.x + self.radius > CANVAS_WIDTH and self.velocity.x > 0.0) \
                or (self.center.x - self.radius < 0.0 and self.velocity.x < 0.0):
            self.velocity.x = -self.velocity.x
        if (self.center.y + self.radius > CANVAS_HEIGHT and self.velocity.y > 0.0) \
                or (self.center.y - self.radius < 0.0 and self.velocity.y < 0.0):
            self.velocity.y = -self.velocity.y

    def render(self, canvas):
        canvas.coords(self.id, [self.bounding_box.x1, self.bounding_box.y1,
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

class Bouncy_World:
    def __init__(self):
        self.size = 0
        self.ball_array = []

        self.board = tk.Tk()
        self.board.title('bouncy world')

        self.canvas = tk.Canvas(self.board, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='ivory')
        self.canvas.pack()

    def add_ball(self, ball):
        self.ball_array.append(ball)
        self.size += 1

    def mainloop(self):
        while True:
            tm.sleep(DELTA_TIME)

            self._update()
            self._render()
            self._ball_collide()

    def _update(self):
        ''' ball attributes update '''
        for ball in self.ball_array:
            ball.update()

    def _render(self):
        ''' ball render '''
        for ball in self.ball_array:
            ball.render(self.canvas)

        self._draw_call()

    def _draw_call(self):
        ''' draw elements on canvas '''
        self.canvas.update_idletasks()
        self.canvas.update()

    def _ball_collide(self):
        for i, b1 in enumerate(self.ball_array):
            for j, b2 in enumerate(self.ball_array[(i + 1):]):
                collide_vector = Point(b2.center.x - b1.center.x,
                                       b2.center.y - b1.center.y)

                distance = mt.sqrt(pow2(collide_vector.x) + pow2(collide_vector.y))
                if distance > (b1.radius + b2.radius):
                    continue

                sin_theta = collide_vector.y / distance
                cos_theta = collide_vector.x / distance

                b1_normal_velocity  =   b1.velocity.x * cos_theta \
                                      + b1.velocity.y * sin_theta
                b1_tangent_velocity =   b1.velocity.x * sin_theta \
                                      + b1.velocity.y * cos_theta
                b2_normal_velocity  =   b2.velocity.x * cos_theta \
                                      + b2.velocity.y * sin_theta
                b2_tangent_velocity =   b2.velocity.x * sin_theta \
                                      + b2.velocity.y * cos_theta

                b1_momentum = b1.mass * b1_normal_velocity
                b2_momentum = b2.mass * b2_normal_velocity
                denom = b1.mass + b2.mass
                b1_nom = (b1.mass - b2.mass) * b1_normal_velocity + 2 * b2_momentum
                b2_nom = (b2.mass - b1.mass) * b2_normal_velocity + 2 * b1_momentum
                b1_normal_velocity = b1_nom / denom
                b2_normal_velocity = b2_nom / denom

                b1.velocity.x =   b1_normal_velocity  * cos_theta \
                                + b1_tangent_velocity * sin_theta
                b1.velocity.y =   b1_normal_velocity  * sin_theta \
                                + b1_tangent_velocity * cos_theta
                b2.velocity.x =   b2_normal_velocity  * cos_theta \
                                + b2_tangent_velocity * sin_theta
                b2.velocity.y =   b2_normal_velocity  * sin_theta \
                                + b2_tangent_velocity * cos_theta


# Entrance
if __name__ == '__main__':
    bouncy_world = Bouncy_World()
    for i in range(BOUNCY_BALL_NUM):
        bouncy_ball = Bouncy_Ball(bouncy_world.canvas, 20, 10, 400 - 40 + i * 40, 100, -80.0 + i * 40.0, 20.0 * i)
        bouncy_world.add_ball(bouncy_ball)

    bouncy_world.mainloop()

