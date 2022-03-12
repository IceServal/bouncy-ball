import util.shapes


class Physical_Ball(util.shapes.Circle):
    ''' a ball has basically physical attributes '''

    def __init__(
        self
        , center: util.shapes.Point
        , radius: float
        , density: float
        , velocity: util.shapes.Point
    ):
        super().__init__(center, radius)

        self.density  = density
        self.mass     = density * self.area()
        self.velocity = velocity

