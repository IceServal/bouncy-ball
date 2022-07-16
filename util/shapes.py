import util.ops
import util.constants


class Shape:
    def __init__(self):
        pass

    def deploy(self, x: float, y: float) -> None:
        pass

    def shift(self, x: float, y: float) -> None:
        pass

    def scale(self, ratio: float) -> None:
        pass

    def area(self) -> float:
        return 0.0

class Point(Shape):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def deploy(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def shift(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

class Vector(Shape):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def deploy(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def shift(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

    def scale(self, ratio: float) -> None:
        self.x *= x
        self.y *= y

    def modulus(self) -> float:
        return util.ops.sqrt(util.ops.pow2(self.x) + util.ops.pow2(self.y))

class Rectangle(Shape):
    def __init__(self, left_up: Point, right_bottom: Point):
        self.left_up      = left_up
        self.right_bottom = right_bottom

        self.x1 = left_up.x
        self.y1 = left_up.y
        self.x2 = right_bottom.x
        self.y2 = right_bottom.y

        self.center = Point(
            util.ops.mean2(self.x1, self.x2),
            util.ops.mean2(self.y1, self.y2)
        )

        self.width  = abs(right_bottom.x - left_up.x)
        self.height = abs(right_bottom.y - left_up.y)
        self.radius = Point(self.width / 2.0, self.height / 2.0)

    def deploy(self, x: float, y: float) -> None:
        self.left_up.deploy(x - self.radius.x, y - self.radius.y)
        self.right_bottom.deploy(x + self.radius.x, y + self.radius.y)

        self.x1 = self.left_up.x
        self.y1 = self.left_up.y
        self.x2 = self.right_bottom.x
        self.y2 = self.right_bottom.y

        self.center.deploy(x, y)

    def shift(self, x: float, y: float) -> None:
        self.left_up.shift(x, y)
        self.right_bottom.shift(x, y)

        self.x1 += x
        self.y1 += y
        self.x2 += x
        self.y2 += y

        self.center.shift(x, y)

    def scale(self, ratio: float) -> None:
        self.width  *= ratio
        self.height *= ratio

        radius = self.radius
        self.radius.scale(ratio)
        self.left_up.shift(radius.x - self.radius.x, radius.y - self.radius.y)
        self.right_bottom.shift(self.radius.x - radius.x, self.radius.y - radius.y)

        self.x1 = self.left_up.x
        self.y1 = self.left_up.y
        self.x2 = self.right_bottom.x
        self.y2 = self.right_bottom.y

    def area(self) -> float:
        return self.width * self.height

class Circle(Shape):
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def deploy(self, x: float, y: float) -> None:
        self.center.x = x
        self.center.y = y

    def shift(self, x: float, y: float) -> None:
        self.center.x += x
        self.center.y += y

    def scale(self, ratio: float) -> None:
        self.radius *= ratio

    def area(self) -> float:
        return util.constants.PI * util.ops.pow2(self.radius)

