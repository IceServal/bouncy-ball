import tkinter

import scene.constants
import scene.draw_command

class Scene:
    def __init__(self, width: int, height: int):
        self._width  = width * scene.constants.SCALE
        self._height = width * scene.constants.SCALE

        self._board = tkinter.Tk()
        self._board.title('2D particle world')

        self._canvas = tkinter.Canvas(self.board, width=self.width, height=self.height, bg='ivory')
        self._canvas.pack()

        self._draw_command_queue = []

    def enqueue_draw_command(self, cmd: scene.draw_command.Draw_Command) -> None:
        self.draw_command_queue.append(cmd)

    def resize_scene(self, width: int, height: int):
        pass

    def mainloop(self) -> None:
        while True:
            self._update()
            self._render()

    def _update(self) -> None:
        pass

    def _render(self) -> None:
        for cmd in self.draw_command_queue:
            self.canvas.coords(







