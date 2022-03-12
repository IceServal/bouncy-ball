import tkinter

import resource.balls
import resource.constants
import util.shapes


class Mesh:
    def __init__(self, ball: resource.balls.Physical_Ball):
        self.ball = ball
        self.canvas = None
        self.border_width = 0.0
        self.id = None

        left_up      = util.shapes.Point(ball.center.x - ball.radius, ball.center.y - ball.radius)
        right_bottom = util.shapes.Point(ball.center.x + ball.radius, ball.center.y + ball.radius)
        self.bounding_box = util.shapes.Rectangle(left_up, right_bottom)

    def set_canvas(self, canvas: tkinter.Canvas) -> None:
        self.canvas = canvas

    def set_border_width(self, border_width: float) -> None:
        if border_width < 0.0:
            print('WARNING: border width can not less than 0.0')
            print('    Automatically set it with 0.0')
            border_width = 0.0

        self.border_width = border_width

    def create(self) -> None:
        if self.canvas is None:
            print('No canvas to draw, use `set_canvas` method to set it.\n')
            return
        if self.border_width == 0.0:
            print('WARNING: mesh border width is 0.0 which may be not correct.\n')
            print('    Consider use `set_border_width` method to set it.\n')

        self.id = self.canvas.create_oval(
            self.bounding_box.x1 * resource.constants.SCALE,
            self.bounding_box.y1 * resource.constants.SCALE,
            self.bounding_box.x2 * resource.constants.SCALE,
            self.bounding_box.y2 * resource.constants.SCALE,
            width=self.border_width
        )

    def draw(self) -> None:
        if self.canvas is None:
            print('No canvas to draw, use `set_canvas` method to set it.\n')
            return
        if self.id is None:
            print('No oval created, use `create` method to create it.\n')
            return

        self.canvas.coords(
            self.id,
            [
                self.bounding_box.x1 * resource.constants.SCALE,
                self.bounding_box.y1 * resource.constants.SCALE,
                self.bounding_box.x2 * resource.constants.SCALE,
                self.bounding_box.y2 * resource.constants.SCALE,
            ]
        )

