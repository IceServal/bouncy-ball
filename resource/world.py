import time
import tkinter

import resource.constants
import resource.mesh
import util.shapes


class World:
    def __init__(self, width: int, height: int):
        self.width  = width
        self.height = height

        self.board = tkinter.Tk()
        self.board.title('2D ball world')

        canvas_width  = width * resource.constants.SCALE
        canvas_height = height * resource.constants.SCALE
        self.canvas = tkinter.Canvas( self.board, width=canvas_width, height=canvas_height, bg='ivory')
        self.canvas.pack()

        self.mesh_array = []

    def add_mesh(self, mesh: resource.mesh.Mesh) -> None:
        self.mesh_array.append(mesh)

    def mainloop(self) -> None:
        for mesh in self.mesh_array:
            mesh.set_canvas(self.canvas)
            mesh.create()

        while True:
            time.sleep(resource.constants.DELTA_TIME)

            self._update()
            self._render()

    def _update(self) -> None:
        ''' mesh update '''
        self._ball_gravity()
        self._ball_collide_wall()
        self._ball_collide_ball()
        self._ball_shift()

    def _render(self) -> None:
        ''' mesh render '''
        for mesh in self.mesh_array:
            mesh.draw()

        self.canvas.update_idletasks()
        self.canvas.update()

    def _ball_gravity(self) -> None:
        # need add bit condition
        delta_y_speed = resource.constants.GRAVITY * resource.constants.DELTA_TIME
        for mesh in self.mesh_array:
            mesh.ball.velocity.shift(0.0, delta_y_speed)

    def _ball_collide_wall(self) -> None:
        # need add wall resource
        # need add bit condition
        for mesh in self.mesh_array:
            if  False \
                or (mesh.ball.center.x + mesh.ball.radius > self.width and mesh.ball.velocity.x > 0.0) \
                or (mesh.ball.center.x - mesh.ball.radius < 0.0 and mesh.ball.velocity.x < 0.0) \
            :
                mesh.ball.velocity.x = -mesh.ball.velocity.x
            if False \
                or (mesh.ball.center.y + mesh.ball.radius > self.height and mesh.ball.velocity.y > 0.0) \
                or (mesh.ball.center.y - mesh.ball.radius < 0.0 and mesh.ball.velocity.y < 0.0) \
            :
                mesh.ball.velocity.y = -mesh.ball.velocity.y

    def _ball_collide_ball(self) -> None:
        # need add bit condition
        for i, m1 in enumerate(self.mesh_array):
            for j, m2 in enumerate(self.mesh_array[(i + 1):]):
                b1 = m1.ball
                b2 = m2.ball

                delta_position = util.shapes.Vector(
                    b2.center.x - b1.center.x,
                    b2.center.y - b1.center.y
                )
                delta_velocity = util.shapes.Vector(
                    b2.velocity.x - b1.velocity.x,
                    b2.velocity.y - b1.velocity.y
                )
                if True \
                    and ((delta_position.x * delta_velocity.x) >= 0) \
                    and ((delta_position.y * delta_velocity.y) >= 0) \
                :
                    continue

                distance = delta_position.modulus()
                if distance > (m1.ball.radius + m2.ball.radius):
                    continue
                if distance == 0.0:
                    continue
                # need fix bug condition

                sin_theta = delta_position.y / distance
                cos_theta = delta_position.x / distance

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

                m1.ball.velocity.x =   b1_normal_velocity  * cos_theta \
                                     + b1_tangent_velocity * sin_theta
                m1.ball.velocity.y =   b1_normal_velocity  * sin_theta \
                                     + b1_tangent_velocity * cos_theta
                m2.ball.velocity.x =   b2_normal_velocity  * cos_theta \
                                     + b2_tangent_velocity * sin_theta
                m2.ball.velocity.y =   b2_normal_velocity  * sin_theta \
                                     + b2_tangent_velocity * cos_theta

    def _ball_shift(self) -> None:
        for mesh in self.mesh_array:
            delta_position   = util.shapes.Vector(0.0, 0.0)
            delta_position.x = mesh.ball.velocity.x * resource.constants.DELTA_TIME
            delta_position.y = mesh.ball.velocity.y * resource.constants.DELTA_TIME

            mesh.ball.shift(delta_position.x, delta_position.y)
            mesh.bounding_box.shift(delta_position.x, delta_position.y)

