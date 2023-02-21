import pyglet
from constants import *
import sys


class Player():
    def __init__(self, x: int, y: int, batch=None) -> None:
        self.x = x
        self.y = y
        self.batch = batch
        self.position = self.x, self.y
        self._rect = pyglet.shapes.Rectangle(self.x, self.y, 25, 25, color=(255, 255, 0), batch=self.batch)
        self.name_text = pyglet.text.Label(x = x, y = y+25, align="center", batch=self.batch)
        self.direction = [0,0]
        self.dash_cooldown = 2
        self.dash_duration = .2
        self._max_dash_duration = .2
        self._is_dashing = False

    def _update_pos(self, x, y, scroll):
        self.x = x
        self.y = y
        self.position = int(self.x), int(self.y)
        self._rect.x = x - scroll[0]
        self._rect.y = y - scroll[1]
        self.name_text.x = x - scroll[0]
        self.name_text.y = y - scroll[1] - 25

    def dash(self, speed: int, direction: list|tuple[float | int, float | int], t :float, scroll: tuple, total_t: float|int = 1) -> float:
        if total_t <= 0:
            return self._max_dash_duration
        x = self.x + speed * direction[0] * t
        y = self.y + speed * direction[1] * t

        self._update_pos(x, y, scroll)
        return total_t-t if total_t-t > 0 else self._max_dash_duration

    def handle_movement(self, keyboard, mousehandler, dt, scroll):
        from pyglet.window import key
        from pyglet.window import mouse

        if self.dash_cooldown > 0: self.dash_cooldown -= dt

        if (mousehandler[mouse.LEFT] and self.dash_cooldown <= 0) or self.dash_duration != self._max_dash_duration:
            self.dash_cooldown = 2
            self.dash_duration = self.dash(SPEED*2, self.direction, dt, scroll, self.dash_duration)
            self._is_dashing = True
        else:
            self._is_dashing = False

        if keyboard[key.W]:
            self.direction[1] = 1

        elif keyboard[key.S]:
            self.direction[1] = -1

        else:
            self.direction[1] = 0

        if keyboard[key.A]:
            self.direction[0] = -1

        elif keyboard[key.D]:
            self.direction[0] = 1

        else:
            self.direction[0] = 0

        if keyboard[key.Q]:
            sys.exit()


        if self.direction[0] and self.direction[1]:
            self.direction = [i/2 for i in self.direction] #TODO ask leon about this lmao
            x = self.x + self.direction[0] * SPEED * dt
            y = self.y + self.direction[1] * SPEED * dt

        else:
            x = self.x + self.direction[0] * SPEED * dt
            y = self.y + self.direction[1] * SPEED * dt


        self._update_pos(x, y, scroll)
