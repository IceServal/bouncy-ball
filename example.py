import resource.world
import resource.balls
import resource.mesh
import util.shapes


# Global Variables
WORLD_WIDTH  = 8
WORLD_HEIGHT = 8
BALL_NUM = 5


if __name__ == '__main__':
    world = resource.world.World(WORLD_WIDTH, WORLD_HEIGHT)
    for i in range(BALL_NUM):
        center = util.shapes.Point(4.0 + ((i - (BALL_NUM // 2.0)) * 0.5), 2.0)
        radius = 0.2
        density = 2.0
        velocity = util.shapes.Vector(-2.0 + (i * 1.0), i * 1.0)
        ball = resource.balls.Physical_Ball(center, radius, density, velocity)

        mesh = resource.mesh.Mesh(ball)
        mesh.set_border_width(1.0)
        world.add_mesh(mesh)

    world.mainloop()

