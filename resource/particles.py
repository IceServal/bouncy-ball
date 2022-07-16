import util.shapes


class Particle(util.shapes.Circle):
    ''' particle is a kind of circle which has basically 2D physical attributes '''

    def __init__(
        self
        , center: util.shapes.Point
        , radius: float
        , mass: float
        , velocity: util.shapes.Vector
    ):
        super().__init__(center, radius)

        self.mass = mass
        self.velocity = velocity

